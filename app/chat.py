"""
Streamlit chat interface for the EU AI Act RAG system.
Provides an interactive chat experience with citation support and conversation history.
"""

import streamlit as st
from core.rag_chain import load_rag_chain, query_rag_chain
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_session_state():
    """Initialize session state variables for chat history."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None

def load_rag_chain_safely():
    """Safely load the RAG chain with error handling."""
    try:
        if st.session_state.rag_chain is None:
            with st.spinner("Loading AI assistant..."):
                st.session_state.rag_chain = load_rag_chain()
            st.success("AI assistant loaded successfully!")
        return st.session_state.rag_chain
    except Exception as e:
        st.error(f"Failed to load AI assistant: {str(e)}")
        logger.error(f"Error loading RAG chain: {e}")
        return None

def format_citations(text: str) -> str:
    """Format citations in the text to make them more visible."""
    import re
    
    # Highlight article citations
    text = re.sub(r'(Article\s+\d+)', r'**\1**', text)
    text = re.sub(r'(Recital\s+\d+)', r'**\1**', text)
    text = re.sub(r'(Chapter\s+\d+)', r'**\1**', text)
    text = re.sub(r'(Section\s+\d+)', r'**\1**', text)
    
    # Highlight "According to" citations
    text = re.sub(r'(According to\s+[^.]*\.)', r'*"\1"*', text)
    text = re.sub(r'(As stated in\s+[^.]*\.)', r'*"\1"*', text)
    
    return text

def display_source_documents(sources: List[Any], question: str):
    """Display source documents in an expandable section."""
    if not sources:
        return
    
    with st.expander(f"📚 Source Documents ({len(sources)} chunks)", expanded=False):
        st.write("**Retrieved chunks used to answer your question:**")
        
        for i, doc in enumerate(sources, 1):
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
            section = metadata.get('section', 'Unknown Section')
            source = metadata.get('source', 'Unknown Source')
            chunk_id = metadata.get('chunk_id', i)
            
            st.markdown(f"""
            **Document {i}** - {section}
            *Source: {source} | Chunk ID: {chunk_id}*
            
            {doc.page_content[:300]}{'...' if len(doc.page_content) > 300 else ''}
            ---
            """)

def process_user_message(user_message: str) -> Dict[str, Any]:
    """Process user message through the RAG chain."""
    try:
        chain = load_rag_chain_safely()
        if chain is None:
            return {
                "success": False,
                "error": "Failed to load AI assistant"
            }
        
        with st.spinner("🤔 Thinking..."):
            answer, source_docs = query_rag_chain(chain, user_message)
        
        return {
            "success": True,
            "answer": answer,
            "source_documents": source_docs
        }
    
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }

def render():
    """Main render function for the chat interface."""
    st.header("💬 Chat with EU AI Act Assistant")
    st.markdown("Ask questions about the European Union AI Act and get detailed, citation-backed answers.")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar with hints
    with st.sidebar:
        st.markdown("### 💡 Try asking:")
        st.markdown("""
        - What is considered unacceptable AI?
        - What are the obligations for high-risk systems?
        - How are AI systems classified?
        - What are the penalties for non-compliance?
        - What is the definition of AI system?
        """)
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This assistant uses Retrieval-Augmented Generation (RAG) to provide accurate answers based on the EU AI Act regulation.
        
        All responses include citations to specific articles and sections.
        """)
    
    # Load RAG chain
    chain = load_rag_chain_safely()
    if chain is None:
        st.error("❌ Unable to load AI assistant. Please check your configuration and try again.")
        return
    
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.write(message["content"])
            else:
                # Format and display AI response with citations
                formatted_response = format_citations(message["content"])
                st.markdown(formatted_response)
                
                # Display source documents if available
                if "source_documents" in message and message["source_documents"]:
                    display_source_documents(message["source_documents"], message.get("question", ""))
    
    # Chat input
    if prompt := st.chat_input("Ask about the EU AI Act..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Process message through RAG chain
        result = process_user_message(prompt)
        
        # Display AI response
        with st.chat_message("assistant"):
            if result["success"]:
                # Format and display the answer
                formatted_answer = format_citations(result["answer"])
                st.markdown(formatted_answer)
                
                # Add AI response to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": result["answer"],
                    "source_documents": result["source_documents"],
                    "question": prompt
                })
                
                # Display source documents
                display_source_documents(result["source_documents"], prompt)
                
            else:
                st.error(f"❌ {result['error']}")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"Sorry, I encountered an error: {result['error']}"
                })
    
    # Default message if no conversation yet
    if not st.session_state.messages:
        st.info("👋 Welcome! I'm your EU AI Act assistant. Ask me anything about the regulation and I'll provide detailed, citation-backed answers.")
        
        # Example questions
        st.markdown("### 🚀 Get started with these examples:")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("What is the EU AI Act?"):
                st.session_state.messages.append({"role": "user", "content": "What is the EU AI Act?"})
                st.rerun()
        
        with col2:
            if st.button("What are high-risk AI systems?"):
                st.session_state.messages.append({"role": "user", "content": "What are high-risk AI systems?"})
                st.rerun()
    
    # Clear conversation button
    if st.session_state.messages:
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = []
            st.rerun() 