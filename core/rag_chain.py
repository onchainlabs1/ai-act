"""
RAG Chain implementation for EU AI Act using LangChain v0.2 Expression Language (LCEL).
This module provides the core question-answering functionality with citation support.
"""

import os
from typing import Dict, List, Tuple, Any
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langsmith import Client
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_chroma_vectorstore() -> Chroma:
    """
    Load the Chroma vectorstore from the persistent directory.
    
    Returns:
        Chroma: Loaded vectorstore instance
    """
    try:
        # Define the path to the Chroma vectorstore
        vectorstore_path = "vectorstore/chroma"
        
        # Initialize OpenAI embeddings for the vectorstore
        embeddings = OpenAIEmbeddings()
        
        # Load the existing Chroma vectorstore
        vectorstore = Chroma(
            persist_directory=vectorstore_path,
            embedding_function=embeddings
        )
        
        logger.info(f"Successfully loaded Chroma vectorstore from {vectorstore_path}")
        return vectorstore
        
    except Exception as e:
        logger.error(f"Error loading Chroma vectorstore: {e}")
        raise

def format_documents(docs: List[Document]) -> str:
    """
    Format retrieved documents into a context string for the prompt.
    
    Args:
        docs: List of Document objects from the retriever
        
    Returns:
        str: Formatted context string with document content and metadata
    """
    formatted_docs = []
    
    for i, doc in enumerate(docs, 1):
        # Extract metadata for citation
        metadata = doc.metadata
        section = metadata.get('section', 'Unknown Section')
        source = metadata.get('source', 'Unknown Source')
        chunk_id = metadata.get('chunk_id', i)
        
        # Format each document with metadata for citation
        formatted_doc = f"[Document {i} - {section}]\n{doc.page_content}\n"
        formatted_docs.append(formatted_doc)
    
    return "\n".join(formatted_docs)

def create_rag_prompt() -> ChatPromptTemplate:
    """
    Create the prompt template for the RAG chain with system message and placeholders.
    
    Returns:
        ChatPromptTemplate: Configured prompt template
    """
    system_message = """You are an assistant that helps users understand the EU AI Act. 
Use the provided context to answer questions accurately and comprehensively. 
If the information is not available in the provided context, say you don't know rather than making up information.
Always cite the specific article, section, or document when providing information.
Format citations as "According to [Article/Section X]" or "As stated in [Document Y]".
Be concise but thorough in your explanations."""

    human_message = """Context information:
{context}

Question: {question}

Please provide a comprehensive answer based on the context above."""

    return ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", human_message)
    ])

def setup_langsmith_tracing() -> None:
    """
    Configure LangSmith tracing for the RAG chain.
    """
    try:
        # Check if LangSmith is configured via environment variables
        if os.getenv("LANGCHAIN_API_KEY"):
            logger.info("LangSmith tracing is configured and enabled")
        else:
            logger.warning("LangSmith API key not found. Tracing will be disabled.")
    except Exception as e:
        logger.warning(f"Error setting up LangSmith tracing: {e}")

def load_rag_chain() -> Any:
    """
    Load and configure the complete RAG chain using LCEL.
    
    Returns:
        Runnable: Configured LCEL chain ready for question answering
    """
    try:
        # Setup LangSmith tracing
        setup_langsmith_tracing()
        
        # Load the Chroma vectorstore
        vectorstore = load_chroma_vectorstore()
        
        # Create retriever with k=4 documents
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        
        # Create the prompt template
        prompt = create_rag_prompt()
        
        # Initialize the LLM
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,  # Low temperature for factual responses
            max_tokens=1000
        )
        
        # Build the LCEL chain
        # Step 1: Retrieve relevant documents
        retrieval_chain = RunnablePassthrough.assign(
            context=RunnableLambda(lambda x: retriever.get_relevant_documents(x["question"]))
        )
        
        # Step 2: Format documents and create final input
        formatting_chain = RunnableLambda(
            lambda x: {
                "context": format_documents(x["context"]),
                "question": x["question"]
            }
        )
        
        # Step 3: Generate response with LLM
        response_chain = prompt | llm | StrOutputParser()
        
        # Combine all steps into the final chain
        rag_chain = (
            retrieval_chain
            | formatting_chain
            | response_chain
        )
        
        # Name the chain for LangSmith tracking
        rag_chain = rag_chain.with_config({"run_name": "eu_ai_act_rag"})
        
        logger.info("RAG chain 'eu_ai_act_rag' successfully loaded and configured")
        return rag_chain
        
    except Exception as e:
        logger.error(f"Error loading RAG chain: {e}")
        raise

def query_rag_chain(chain: Any, question: str) -> Tuple[str, List[Document]]:
    """
    Execute a query using the RAG chain and return both answer and source documents.
    
    Args:
        chain: The loaded RAG chain
        question: User's question
        
    Returns:
        Tuple[str, List[Document]]: (answer, source_documents)
    """
    try:
        # Execute the chain
        answer = chain.invoke({"question": question})
        
        # Get source documents for citation
        vectorstore = load_chroma_vectorstore()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        source_docs = retriever.get_relevant_documents(question)
        
        logger.info(f"Successfully processed question: {question[:50]}...")
        return answer, source_docs
        
    except Exception as e:
        logger.error(f"Error querying RAG chain: {e}")
        raise

# Example usage function for testing
def test_rag_chain():
    """
    Test function to verify the RAG chain is working correctly.
    """
    try:
        chain = load_rag_chain()
        test_question = "What is the purpose of the EU AI Act?"
        answer, sources = query_rag_chain(chain, test_question)
        
        print(f"Question: {test_question}")
        print(f"Answer: {answer}")
        print(f"Number of source documents: {len(sources)}")
        
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    # Run test if module is executed directly
    test_rag_chain() 