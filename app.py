import streamlit as st
from utils import (
    get_huggingface_client,
    generate_technical_questions,
    analyze_candidate_response,
    generate_follow_up_question,
    validate_candidate_info
)
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="TalentScout - AI-Powered Technical Interview Assistant",
    page_icon="👨‍💻",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "candidate_info" not in st.session_state:
    st.session_state.candidate_info = None
if "interview_stage" not in st.session_state:
    st.session_state.interview_stage = "initial"

# Check for API key
try:
    client = get_huggingface_client()
except ValueError as e:
    st.error("Hugging Face API key not found! Please set your HUGGINGFACE_API_KEY in the .env file.")
    st.stop()

# Main title and description
st.title("👨‍💻 TalentScout")
st.markdown("""
    Welcome to TalentScout, your AI-powered technical interview assistant. 
    This tool helps streamline the initial screening process by:
    - Gathering candidate information
    - Conducting technical assessments
    - Analyzing responses
    - Providing structured feedback
""")

# Sidebar for candidate information
with st.sidebar:
    st.header("Candidate Information")
    
    if st.session_state.interview_stage == "initial":
        candidate_info = {
            "full_name": st.text_input("Full Name"),
            "email": st.text_input("Email"),
            "phone": st.text_input("Phone"),
            "experience": st.number_input("Years of Experience", min_value=0, max_value=50),
            "position": st.text_input("Position Applied For"),
            "location": st.text_input("Location"),
            "tech_stack": st.text_input("Tech Stack (comma-separated)")
        }
        
        if st.button("Start Interview"):
            validated_info = validate_candidate_info(candidate_info)
            st.session_state.candidate_info = validated_info
            st.session_state.interview_stage = "technical"
            st.experimental_rerun()
    
    elif st.session_state.interview_stage == "technical":
        st.write("### Current Candidate")
        st.write(f"**Name:** {st.session_state.candidate_info['full_name']}")
        st.write(f"**Position:** {st.session_state.candidate_info['position']}")
        st.write(f"**Experience:** {st.session_state.candidate_info['experience']} years")
        st.write(f"**Tech Stack:** {', '.join(st.session_state.candidate_info['tech_stack'])}")
        
        if st.button("End Interview"):
            st.session_state.interview_stage = "initial"
            st.session_state.messages = []
            st.session_state.current_question = None
            st.session_state.candidate_info = None
            st.experimental_rerun()

# Main interview interface
if st.session_state.interview_stage == "technical":
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Generate initial questions if none exist
    if not st.session_state.current_question:
        questions = generate_technical_questions(
            tech_stack=st.session_state.candidate_info["tech_stack"],
            experience=st.session_state.candidate_info["experience"]
        )
        st.session_state.questions = questions
        st.session_state.current_question_index = 0
        st.session_state.current_question = questions[0]
        st.session_state.technical_analysis = []
        st.session_state.is_relevant = True
    
    st.write(f"**Question {st.session_state.current_question_index + 1}/{len(st.session_state.questions)}:**")
    st.write(st.session_state.current_question)
    
    # Store the current question in context
    context = {
        "tech_stack": st.session_state.candidate_info["tech_stack"],
        "experience": st.session_state.candidate_info["experience"],
        "current_question": st.session_state.current_question,
        "previous_questions": st.session_state.questions[:st.session_state.current_question_index],
        "previous_analysis": st.session_state.technical_analysis
    }
    
    # Get candidate's response
    response = st.text_area("Your answer:", key=f"response_{st.session_state.current_question_index}")
    
    if st.button("Submit Answer"):
        if response:
            # Analyze the response
            analysis = analyze_candidate_response(response, st.session_state.current_question)
            st.session_state.technical_analysis.append(analysis)
            
            # Display analysis
            st.write("**Analysis:**")
            st.write(analysis["analysis"])
            
            # Generate follow-up question if response is relevant
            if analysis["is_relevant"]:
                follow_up = generate_follow_up_question(response, context, is_relevant=True)
                st.write("**Follow-up Question:**")
                st.write(follow_up)
                
                # Get follow-up response
                follow_up_response = st.text_area("Your answer to the follow-up:", key=f"follow_up_{st.session_state.current_question_index}")
                
                if st.button("Submit Follow-up Answer"):
                    if follow_up_response:
                        # Analyze follow-up response
                        follow_up_analysis = analyze_candidate_response(follow_up_response, follow_up)
                        st.session_state.technical_analysis.append(follow_up_analysis)
                        
                        # Display follow-up analysis
                        st.write("**Follow-up Analysis:**")
                        st.write(follow_up_analysis["analysis"])
                        
                        # Move to next question
                        st.session_state.current_question_index += 1
                        if st.session_state.current_question_index < len(st.session_state.questions):
                            st.session_state.current_question = st.session_state.questions[st.session_state.current_question_index]
                            st.experimental_rerun()
                        else:
                            st.session_state.interview_stage = "summary"
                            st.experimental_rerun()
            else:
                # If response is not relevant, ask the same question again
                st.write("**Please provide a response that directly addresses the question.**")
                st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ using Streamlit and Hugging Face AI</p>
        <p>Version 1.0.0</p>
    </div>
""", unsafe_allow_html=True) 