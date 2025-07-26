import streamlit as st

st.set_page_config(page_title="AI Act Tutor", layout="wide")

st.title("AI Act Tutor")

PAGES = {
    "Chat": "Chat with the EU AI Act",
    "Study": "Guided Study Modules",
    "Quiz": "Quiz Yourself"
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

if selection == "Chat":
    from app import chat
    chat.render()
elif selection == "Study":
    from app import study
    study.render()
elif selection == "Quiz":
    from app import quiz
    quiz.render() 