"""
Quiz Mode page for the AI Act Tutor application.
Provides interactive multiple-choice quizzes to test knowledge of the EU AI Act.
"""

import streamlit as st
import json
from typing import Dict, List, Any
import random

def initialize_session_state():
    """Initialize session state for quiz functionality."""
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    
    if "quiz_completed" not in st.session_state:
        st.session_state.quiz_completed = False
    
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

def load_quiz_questions() -> List[Dict[str, Any]]:
    """Load predefined quiz questions about the EU AI Act."""
    
    questions = [
        {
            "id": 1,
            "question": "What is the main objective of the EU AI Act?",
            "options": [
                "To ban all AI systems in the EU",
                "To establish a comprehensive legal framework for AI systems",
                "To promote only high-risk AI systems",
                "To regulate only AI research"
            ],
            "correct_answer": 1,
            "explanation": "The EU AI Act establishes a comprehensive legal framework for AI systems, focusing on risk-based regulation rather than banning AI or regulating only specific types.",
            "category": "Introduction"
        },
        {
            "id": 2,
            "question": "How many risk categories are defined in the EU AI Act?",
            "options": [
                "2 categories",
                "3 categories", 
                "4 categories",
                "5 categories"
            ],
            "correct_answer": 2,
            "explanation": "The EU AI Act defines 4 risk categories: unacceptable risk, high risk, limited risk, and minimal risk.",
            "category": "Risk Categories"
        },
        {
            "id": 3,
            "question": "Which of the following is considered an unacceptable AI practice?",
            "options": [
                "AI systems for medical diagnosis",
                "AI systems for credit scoring",
                "AI systems that manipulate human behavior to cause harm",
                "AI systems for educational purposes"
            ],
            "correct_answer": 2,
            "explanation": "AI systems that manipulate human behavior to cause harm are explicitly prohibited as unacceptable practices under the EU AI Act.",
            "category": "Prohibited Uses"
        },
        {
            "id": 4,
            "question": "What is required for high-risk AI systems under the EU AI Act?",
            "options": [
                "No special requirements",
                "Only basic documentation",
                "Comprehensive risk management and conformity assessment",
                "Only user notification"
            ],
            "correct_answer": 2,
            "explanation": "High-risk AI systems require comprehensive risk management, conformity assessment, and compliance with strict obligations under the regulation.",
            "category": "High-Risk Obligations"
        },
        {
            "id": 5,
            "question": "What are the maximum penalties for non-compliance with the EU AI Act?",
            "options": [
                "€10,000 or 2% of global turnover",
                "€20,000,000 or 4% of global turnover",
                "€30,000,000 or 6% of global turnover",
                "€40,000,000 or 8% of global turnover"
            ],
            "correct_answer": 1,
            "explanation": "The maximum penalties are €20,000,000 or 4% of global annual turnover, whichever is higher.",
            "category": "Penalties and Enforcement"
        },
        {
            "id": 6,
            "question": "What does GPAI stand for in the context of the EU AI Act?",
            "options": [
                "General Purpose Artificial Intelligence",
                "Global Policy on AI",
                "Government Program for AI",
                "General Practice AI"
            ],
            "correct_answer": 0,
            "explanation": "GPAI stands for General Purpose Artificial Intelligence, which refers to AI models that can be used for multiple purposes.",
            "category": "GPAI Models"
        },
        {
            "id": 7,
            "question": "When did the EU AI Act officially enter into force?",
            "options": [
                "2023",
                "2024",
                "2025",
                "2026"
            ],
            "correct_answer": 1,
            "explanation": "The EU AI Act entered into force in 2024, with different provisions becoming applicable at different times.",
            "category": "Introduction"
        },
        {
            "id": 8,
            "question": "What is the purpose of the AI Office established under the EU AI Act?",
            "options": [
                "To develop AI systems",
                "To coordinate enforcement and provide guidance",
                "To fund AI research",
                "To ban AI systems"
            ],
            "correct_answer": 1,
            "explanation": "The AI Office coordinates enforcement activities and provides guidance on the implementation of the EU AI Act.",
            "category": "Penalties and Enforcement"
        }
    ]
    
    return questions

def display_question(question_data: Dict[str, Any], question_index: int, total_questions: int):
    """Display a single quiz question with options."""
    
    st.markdown(f"### Question {question_index + 1} of {total_questions}")
    st.markdown(f"**Category:** {question_data['category']}")
    st.markdown("---")
    
    # Display the question
    st.markdown(f"**{question_data['question']}**")
    
    # Create radio buttons for options
    user_answer = st.radio(
        "Select your answer:",
        options=question_data['options'],
        key=f"question_{question_data['id']}",
        index=None
    )
    
    return user_answer

def check_answer(user_answer: str, question_data: Dict[str, Any]) -> Dict[str, Any]:
    """Check if the user's answer is correct and provide feedback."""
    
    correct_option = question_data['options'][question_data['correct_answer']]
    is_correct = user_answer == correct_option
    
    return {
        "is_correct": is_correct,
        "correct_answer": correct_option,
        "explanation": question_data['explanation']
    }

def display_feedback(result: Dict[str, Any], user_answer: str):
    """Display feedback for the user's answer."""
    
    if result["is_correct"]:
        st.success("✅ **Correct!** Well done!")
    else:
        st.error(f"❌ **Incorrect.** The correct answer is: **{result['correct_answer']}**")
    
    # Show explanation
    with st.expander("💡 Explanation", expanded=True):
        st.markdown(result["explanation"])

def calculate_score() -> Dict[str, Any]:
    """Calculate the final quiz score and statistics."""
    
    total_questions = len(st.session_state.quiz_questions)
    correct_answers = sum(1 for answer in st.session_state.user_answers.values() if answer["is_correct"])
    score_percentage = (correct_answers / total_questions) * 100
    
    # Determine performance level
    if score_percentage >= 90:
        performance = "Excellent"
        emoji = "🏆"
    elif score_percentage >= 75:
        performance = "Good"
        emoji = "👍"
    elif score_percentage >= 60:
        performance = "Fair"
        emoji = "😊"
    else:
        performance = "Needs Improvement"
        emoji = "📚"
    
    return {
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "score_percentage": score_percentage,
        "performance": performance,
        "emoji": emoji
    }

def display_results():
    """Display the final quiz results."""
    
    st.markdown("## 🎉 Quiz Complete!")
    
    score_data = calculate_score()
    
    # Score display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Questions", score_data["total_questions"])
    
    with col2:
        st.metric("Correct Answers", score_data["correct_answers"])
    
    with col3:
        st.metric("Score", f"{score_data['score_percentage']:.1f}%")
    
    # Performance message
    st.markdown(f"### {score_data['emoji']} {score_data['performance']}")
    
    if score_data["score_percentage"] >= 75:
        st.success("Great job! You have a solid understanding of the EU AI Act.")
    elif score_data["score_percentage"] >= 50:
        st.warning("Good effort! Consider reviewing the study modules to improve your knowledge.")
    else:
        st.info("Keep studying! The EU AI Act is complex - use the study modules to learn more.")
    
    # Detailed results
    with st.expander("📊 Detailed Results", expanded=False):
        for i, (question_id, answer_data) in enumerate(st.session_state.user_answers.items()):
            question = next(q for q in st.session_state.quiz_questions if q['id'] == int(question_id))
            
            status = "✅" if answer_data["is_correct"] else "❌"
            st.markdown(f"**Q{i+1}:** {status} {question['question']}")
    
    # Restart quiz button
    if st.button("🔄 Take Quiz Again"):
        st.session_state.current_question_index = 0
        st.session_state.user_answers = {}
        st.session_state.quiz_completed = False
        st.session_state.quiz_score = 0
        st.rerun()

def render():
    """Main render function for the quiz page."""
    
    # Initialize session state
    initialize_session_state()
    
    # Load questions if not already loaded
    if not st.session_state.quiz_questions:
        st.session_state.quiz_questions = load_quiz_questions()
    
    # Page header
    st.markdown("## 🧠 Quiz Mode")
    st.markdown("Test your knowledge of the EU AI Act with these multiple-choice questions!")
    
    # Quiz instructions
    with st.expander("📋 Quiz Instructions", expanded=False):
        st.markdown("""
        **How to take the quiz:**
        
        • Read each question carefully
        • Select the best answer from the options provided
        • Click "Submit Answer" to check your response
        • Review the explanation for each question
        • Use "Next Question" to continue
        • Your progress is automatically saved
        
        **Scoring:**
        • Each correct answer earns 1 point
        • Your final score is shown as a percentage
        • Performance levels: Excellent (90%+), Good (75%+), Fair (60%+), Needs Improvement (<60%)
        """)
    
    # Check if quiz is completed
    if st.session_state.quiz_completed:
        display_results()
        return
    
    # Progress bar
    progress = (st.session_state.current_question_index + 1) / len(st.session_state.quiz_questions)
    st.progress(progress)
    st.markdown(f"**Progress:** {st.session_state.current_question_index + 1} of {len(st.session_state.quiz_questions)} questions")
    
    # Get current question
    current_question = st.session_state.quiz_questions[st.session_state.current_question_index]
    
    # Display question
    user_answer = display_question(
        current_question, 
        st.session_state.current_question_index, 
        len(st.session_state.quiz_questions)
    )
    
    # Submit answer button
    if user_answer:
        if st.button("✅ Submit Answer"):
            # Check answer
            result = check_answer(user_answer, current_question)
            
            # Store answer
            st.session_state.user_answers[str(current_question['id'])] = {
                "user_answer": user_answer,
                "is_correct": result["is_correct"],
                "correct_answer": result["correct_answer"]
            }
            
            # Display feedback
            display_feedback(result, user_answer)
            
            # Next question or complete quiz
            if st.session_state.current_question_index < len(st.session_state.quiz_questions) - 1:
                if st.button("➡️ Next Question"):
                    st.session_state.current_question_index += 1
                    st.rerun()
            else:
                if st.button("🏁 Complete Quiz"):
                    st.session_state.quiz_completed = True
                    st.rerun()
    
    # Skip question option (for development/testing)
    if st.button("⏭️ Skip Question"):
        st.session_state.current_question_index += 1
        if st.session_state.current_question_index >= len(st.session_state.quiz_questions):
            st.session_state.quiz_completed = True
        st.rerun() 