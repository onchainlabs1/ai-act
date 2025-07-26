"""
Study Modules page for the AI Act Tutor application.
Provides structured learning paths through key topics of the EU AI Act.
"""

import streamlit as st
from core.rag_chain import load_rag_chain, query_rag_chain
import logging
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_session_state():
    """Initialize session state for study modules."""
    if "study_responses" not in st.session_state:
        st.session_state.study_responses = {}
    
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None

def load_rag_chain_safely():
    """Safely load the RAG chain with error handling."""
    try:
        if st.session_state.rag_chain is None:
            with st.spinner("Loading AI assistant..."):
                st.session_state.rag_chain = load_rag_chain()
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

def display_source_documents(sources: List[Any], section_name: str):
    """Display source documents in an expandable section."""
    if not sources:
        return
    
    with st.expander(f"📚 Source Documents for {section_name} ({len(sources)} chunks)", expanded=False):
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

def process_study_question(question: str, section_name: str) -> Dict[str, Any]:
    """Process a study question through the RAG chain."""
    try:
        chain = load_rag_chain_safely()
        if chain is None:
            return {
                "success": False,
                "error": "Failed to load AI assistant"
            }
        
        with st.spinner(f"🤔 Analyzing {section_name}..."):
            answer, source_docs = query_rag_chain(chain, question)
        
        return {
            "success": True,
            "answer": answer,
            "source_documents": source_docs
        }
    
    except Exception as e:
        logger.error(f"Error processing study question: {e}")
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }

def create_study_section(section_name: str, summary: str, question: str, icon: str):
    """Create a collapsible study section with RAG integration."""
    
    with st.expander(f"{icon} {section_name}", expanded=False):
        st.markdown(f"**Summary:** {summary}")
        
        # Check if we already have a response for this section
        section_key = section_name.lower().replace(" ", "_")
        
        if st.button(f"🔍 Explain {section_name} Further", key=f"btn_{section_key}"):
            # Process the question through RAG
            result = process_study_question(question, section_name)
            
            if result["success"]:
                # Store the response
                st.session_state.study_responses[section_key] = result
                st.rerun()
            else:
                st.error(f"❌ {result['error']}")
        
        # Display existing response if available
        if section_key in st.session_state.study_responses:
            response = st.session_state.study_responses[section_key]
            
            st.markdown("---")
            st.markdown("### 🤖 AI Assistant Response")
            
            # Format and display the answer
            formatted_answer = format_citations(response["answer"])
            st.markdown(formatted_answer)
            
            # Display source documents
            display_source_documents(response["source_documents"], section_name)
            
            # Clear response button
            if st.button(f"🗑️ Clear Response", key=f"clear_{section_key}"):
                del st.session_state.study_responses[section_key]
                st.rerun()

def render():
    """Main render function for the study modules page."""
    
    # Initialize session state
    initialize_session_state()
    
    # Page header
    st.markdown("## 📖 Study Modules")
    st.markdown("""
    Explore the key topics of the EU AI Act through structured learning modules. 
    Each section provides a summary and the option to get detailed explanations from our AI assistant.
    """)
    
    # Study sections configuration
    study_sections = [
        {
            "name": "Introduction",
            "summary": "Overview of the EU AI Act, its scope, objectives, and fundamental principles for regulating artificial intelligence systems.",
            "question": "What is the EU AI Act and what are its main objectives and scope?",
            "icon": "🎯"
        },
        {
            "name": "Risk Categories",
            "summary": "Classification of AI systems into different risk categories: unacceptable, high-risk, limited risk, and minimal risk.",
            "question": "How are AI systems classified into different risk categories under the EU AI Act?",
            "icon": "⚠️"
        },
        {
            "name": "High-Risk Obligations",
            "summary": "Comprehensive requirements and obligations for providers and users of high-risk AI systems.",
            "question": "What are the main obligations and requirements for high-risk AI systems under the EU AI Act?",
            "icon": "🔒"
        },
        {
            "name": "Prohibited Uses",
            "summary": "AI practices that are considered unacceptable and prohibited under the regulation.",
            "question": "What AI practices are prohibited and considered unacceptable under the EU AI Act?",
            "icon": "🚫"
        },
        {
            "name": "GPAI Models",
            "summary": "Special provisions for General Purpose AI (GPAI) models and foundation models.",
            "question": "How does the EU AI Act regulate General Purpose AI (GPAI) models and foundation models?",
            "icon": "🧠"
        },
        {
            "name": "Penalties and Enforcement",
            "summary": "Enforcement mechanisms, penalties, and compliance requirements under the regulation.",
            "question": "What are the penalties and enforcement mechanisms under the EU AI Act?",
            "icon": "⚖️"
        }
    ]
    
    # Create study sections
    for section in study_sections:
        create_study_section(
            section["name"],
            section["summary"], 
            section["question"],
            section["icon"]
        )
    
    # Progress tracking
    st.markdown("---")
    st.markdown("### 📊 Your Progress")
    
    completed_sections = len(st.session_state.study_responses)
    total_sections = len(study_sections)
    progress_percentage = (completed_sections / total_sections) * 100
    
    st.progress(progress_percentage / 100)
    st.markdown(f"**Completed:** {completed_sections}/{total_sections} sections ({progress_percentage:.1f}%)")
    
    # Study tips
    with st.expander("💡 Study Tips", expanded=False):
        st.markdown("""
        **Effective Learning Strategies:**
        
        • **Start with Introduction** - Get familiar with the basic concepts first
        • **Read the summaries** - Understand the key points before diving deeper
        • **Ask follow-up questions** - Use the chat assistant for specific clarifications
        • **Review source documents** - Check the citations to understand the legal basis
        • **Take notes** - Keep track of important articles and requirements
        
        **Recommended Study Order:**
        1. Introduction
        2. Risk Categories  
        3. Prohibited Uses
        4. High-Risk Obligations
        5. GPAI Models
        6. Penalties and Enforcement
        """)
    
    # Clear all responses button
    if st.session_state.study_responses:
        if st.button("🗑️ Clear All Responses"):
            st.session_state.study_responses = {}
            st.rerun() 