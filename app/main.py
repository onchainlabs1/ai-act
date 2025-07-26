"""
Main entry point for the AI Act Tutor Streamlit application.
Provides multipage navigation between Chat, Study, and Quiz modules.
"""

import streamlit as st
from app import chat, study, quiz

def main():
    """Main application function with multipage navigation."""
    
    # Configure page settings
    st.set_page_config(
        page_title="AI Act Tutor",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sidebar-header {
        text-align: center;
        color: #2c3e50;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .page-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown('<h2 class="sidebar-header">🤖 AI Act Tutor</h2>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Page selection
        page = st.selectbox(
            "Choose a module:",
            options=[
                "💬 Chat Assistant",
                "📖 Study Modules", 
                "🧠 Quiz Mode"
            ],
            index=0  # Default to Chat Assistant
        )
        
        st.markdown("---")
        
        # App information
        st.markdown("### ℹ️ About")
        st.markdown("""
        **AI Act Tutor** helps you understand the European Union AI Act through:
        
        • **Interactive Chat** - Ask questions and get citation-backed answers
        • **Study Modules** - Guided learning paths through the regulation
        • **Quiz Mode** - Test your knowledge with generated questions
        
        Built with Streamlit and LangChain RAG technology.
        """)
        
        st.markdown("---")
        
        # Quick links
        st.markdown("### 🔗 Quick Links")
        if st.button("📚 EU AI Act Official"):
            st.markdown("[EU AI Act Regulation](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689)")
        
        if st.button("📖 Documentation"):
            st.markdown("[Project README](https://github.com/onchainlabs1/ai-act)")
    
    # Main content area
    st.markdown('<h1 class="main-header">🤖 AI Act Tutor</h1>', unsafe_allow_html=True)
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    
    # Dynamic page loading based on selection
    if page == "💬 Chat Assistant":
        st.markdown("### 💬 Interactive Chat Assistant")
        st.markdown("Ask questions about the EU AI Act and receive detailed, citation-backed answers powered by RAG technology.")
        chat.render()
        
    elif page == "📖 Study Modules":
        st.markdown("### 📖 Study Modules")
        st.markdown("Guided learning paths through the EU AI Act regulation.")
        study.render()
        
    elif page == "🧠 Quiz Mode":
        st.markdown("### 🧠 Quiz Mode")
        st.markdown("Test your knowledge of the EU AI Act with interactive quizzes.")
        quiz.render()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        🤖 AI Act Tutor | Built with Streamlit & LangChain | 
        <a href='https://github.com/onchainlabs1/ai-act' target='_blank'>GitHub</a>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 