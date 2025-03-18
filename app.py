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
if "greeting_sent" not in st.session_state:
    st.session_state.greeting_sent = False

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
            "full_name": st.text_input("Full Name *"),
            "email": st.text_input("Email *"),
            "phone": st.text_input("Phone *"),
            "experience": st.number_input("Years of Experience", min_value=0, max_value=50),
            "position": st.text_input("Position Applied For *"),
            "location": st.text_input("Location"),
            "tech_stack": st.text_input("Tech Stack (comma-separated) *")
        }
        
        if st.button("Start Interview"):
            try:
                validated_info = validate_candidate_info(candidate_info)
                st.session_state.candidate_info = validated_info
                st.session_state.interview_stage = "technical"
                st.experimental_rerun()
            except ValueError as e:
                st.error(str(e))
    
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
            st.session_state.greeting_sent = False
            st.experimental_rerun()

# Main interview interface
if st.session_state.interview_stage == "technical":
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Send greeting message if not sent yet
    if not st.session_state.greeting_sent:
        greeting = f"""Hello {st.session_state.candidate_info['full_name']}! 👋

I'm your technical interview assistant for the {st.session_state.candidate_info['position']} position. 
I'll be conducting a technical assessment based on your experience with {', '.join(st.session_state.candidate_info['tech_stack'])}.

The interview will include:
- Technical questions based on your experience level
- Real-time feedback on your responses
- Follow-up questions to explore your knowledge further

You can end the interview at any time by:
- Clicking the "End Interview" button in the sidebar
- Typing "exit", "quit", or "end interview" in the chat

Let's begin!"""
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": greeting
        })
        st.session_state.greeting_sent = True
        st.experimental_rerun()
    
    # Generate initial questions if none exist
    if not st.session_state.current_question:
        questions = generate_technical_questions(
            tech_stack=st.session_state.candidate_info["tech_stack"],
            experience=st.session_state.candidate_info["experience"]
        )
        st.session_state.current_question = questions[0]
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Let's start with this technical question:\n\n{st.session_state.current_question}"
        })
        st.experimental_rerun()
    
    # Chat input for candidate response
    if prompt := st.chat_input("Type your response here..."):
        # Check for conversation-ending keywords
        if prompt.lower() in ["exit", "quit", "end interview"]:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Thank you for your time! The interview has been ended. You can start a new interview by clicking the 'End Interview' button in the sidebar."
            })
            st.experimental_rerun()
        
        # Add candidate's response to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Analyze the response
        analysis = analyze_candidate_response(prompt, st.session_state.current_question)
        
        # Generate follow-up question
        follow_up = generate_follow_up_question(prompt, {
            "tech_stack": st.session_state.candidate_info["tech_stack"],
            "current_question": st.session_state.current_question
        })
        
        # Update messages with analysis and follow-up
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"**Analysis of your response:**\n{analysis['analysis']}\n\n**Follow-up question:**\n{follow_up}"
        })
        
        # Update current question
        st.session_state.current_question = follow_up
        
        st.experimental_rerun()
