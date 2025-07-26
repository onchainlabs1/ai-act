from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
# TODO: Add LangSmith tracking
# TODO: Add HuggingFaceEmbeddings fallback

def build_rag_chain(vectorstore: Chroma):
    """
    Build a RAG chain for the EU AI Act with citation-friendly prompt.
    Args:
        vectorstore: Chroma vectorstore instance
    Returns:
        LCEL RAG chain
    """
    retriever = vectorstore.as_retriever()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert on the EU AI Act. Always cite the source and article (e.g., 'According to Article 5...'). Be concise and accurate."),
        ("user", "{question}")
    ])
    chain = (
        RunnableMap({
            "context": RunnableLambda(lambda x: retriever.get_relevant_documents(x["question"])) | RunnableLambda(lambda docs: "\n".join([d.page_content for d in docs])),
            "question": RunnablePassthrough()
        })
        | prompt
        | StrOutputParser()
    )
    # TODO: Add LangSmith run tracking (name: 'eu-ai-act-rag')
    return chain 