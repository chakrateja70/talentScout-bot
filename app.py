"""
TalentScout - AI-Powered Technical Interview Assistant

This module implements a Streamlit-based web application for conducting technical interviews.
It provides an interactive interface for gathering candidate information, conducting technical
assessments, and analyzing responses using AI-powered tools.

The application uses Streamlit for the UI and integrates with Hugging Face's API for
AI-powered question generation and response analysis.
"""

import streamlit as st
from utils import (
    get_huggingface_client,
    generate_technical_questions,
    analyze_candidate_response,
    generate_follow_up_question,
    validate_candidate_info,
    evaluate_answer_satisfaction,
    make_api_request
)
import os
from dotenv import load_dotenv
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="TalentScout - AI-Powered Technical Interview Assistant",
    page_icon="👨‍💻",
    layout="wide"
)

# Initialize session state variables for managing interview flow
# messages: Stores the conversation history
# current_question: Tracks the current technical question being asked
# candidate_info: Stores validated candidate information
# interview_stage: Tracks the current stage of the interview (initial/technical)
# greeting_sent: Ensures greeting is sent only once
# questions_asked: Tracks the number of questions asked
# current_topic: Tracks the current topic being discussed
# is_processing: Tracks if we're currently processing a response
# interview_summary: Stores the interview summary and feedback
# show_summary: Controls whether to show the summary
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
if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = 0
if "current_topic" not in st.session_state:
    st.session_state.current_topic = None
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False
if "interview_summary" not in st.session_state:
    st.session_state.interview_summary = None
if "show_summary" not in st.session_state:
    st.session_state.show_summary = False

# Check for API key and initialize Hugging Face client
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
        # Candidate information form with required fields marked with *
        candidate_info = {
            "full_name": st.text_input("Full Name *", placeholder="John Doe"),
            "email": st.text_input("Email *", placeholder="john.doe@example.com"),
            "phone": st.text_input("Phone *", placeholder="+91 XXXXX XXXXX"),
            "experience": st.number_input("Years of Experience", min_value=0, max_value=50, value=0),
            "position": st.text_input("Position Applied For *", placeholder="Senior Software Engineer"),
            "location": st.text_input("Location", placeholder="New York, NY"),
            "tech_stack": st.text_input("Tech Stack (comma-separated) *", placeholder="Python, JavaScript, React, Node.js")
        }
        
        if st.button("Start Interview"):
            try:
                # Validate and store candidate information
                validated_info = validate_candidate_info(candidate_info)
                st.session_state.candidate_info = validated_info
                st.session_state.interview_stage = "technical"
                st.rerun()
            except ValueError as e:
                st.error(str(e))
    
    elif st.session_state.interview_stage == "technical":
        # Display current candidate information during the interview
        st.write("### Current Candidate")
        st.write(f"**Name:** {st.session_state.candidate_info['full_name']}")
        st.write(f"**Position:** {st.session_state.candidate_info['position']}")
        st.write(f"**Experience:** {st.session_state.candidate_info['experience']} years")
        st.write(f"**Tech Stack:** {', '.join(st.session_state.candidate_info['tech_stack'])}")
        st.write(f"**Questions Asked:** {st.session_state.questions_asked}")
        
        if st.button("End Interview"):
            # Generate interview summary and feedback
            with st.spinner("Generating interview summary..."):
                # Extract all assistant messages for analysis
                assistant_messages = [msg for msg in st.session_state.messages if msg["role"] == "assistant"]
                
                # Create a prompt for the summary
                summary_prompt = f"""Generate a comprehensive interview summary for the following candidate:
                Name: {st.session_state.candidate_info['full_name']}
                Position: {st.session_state.candidate_info['position']}
                Experience: {st.session_state.candidate_info['experience']} years
                Tech Stack: {', '.join(st.session_state.candidate_info['tech_stack'])}
                Questions Asked: {st.session_state.questions_asked}
                
                Interview Messages:
                {chr(10).join([msg['content'] for msg in assistant_messages])}
                
                Please provide a structured summary including:
                1. Overall Performance (0-10)
                2. Key Strengths
                3. Areas for Improvement
                4. Technical Knowledge Assessment
                5. Communication Skills
                6. Final Recommendation
                7. Interview Duration
                """
                
                # Generate summary using the API
                messages = [
                    {"role": "system", "content": "You are an expert technical interviewer providing a comprehensive interview summary."},
                    {"role": "user", "content": summary_prompt}
                ]
                
                summary = make_api_request(messages, temperature=0.3)
                st.session_state.interview_summary = summary
                st.session_state.show_summary = True

# Main interview interface
if st.session_state.interview_stage == "technical":
    # Display chat messages with appropriate styling
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Send initial greeting message if not sent yet
    if not st.session_state.greeting_sent:
        greeting = f"""Hello {st.session_state.candidate_info['full_name']}! 👋

I'm your technical interview assistant for the {st.session_state.candidate_info['position']} position. 
I'll be conducting a technical assessment based on your experience with {', '.join(st.session_state.candidate_info['tech_stack'])}.

The interview will include:
- Technical questions based on your experience level
- Real-time feedback on your responses
- Follow-up questions to explore your knowledge further
- Moving to new topics once we've covered a subject thoroughly

You can end the interview at any time by:
- Clicking the "End Interview" button in the sidebar
- Typing "exit", "quit", or "end interview" in the chat

Let's begin!"""
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": greeting
        })
        st.session_state.greeting_sent = True
        st.rerun()
    
    # Generate initial technical questions if none exist
    if not st.session_state.current_question:
        questions = generate_technical_questions(
            tech_stack=st.session_state.candidate_info["tech_stack"],
            experience=st.session_state.candidate_info["experience"]
        )
        st.session_state.current_question = questions[0]
        st.session_state.current_topic = questions[0].split(']')[0].strip('[') if ']' in questions[0] else "General"
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Let's start with this technical question:\n\n{st.session_state.current_question}"
        })
        st.rerun()
    
    # Chat input for candidate response
    if prompt := st.chat_input("Type your response here..."):
        # Check for conversation-ending keywords
        if prompt.lower() in ["exit", "quit", "end interview"]:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Thank you for your time! The interview has been ended. You can start a new interview by clicking the 'End Interview' button in the sidebar."
            })
            st.rerun()
        
        # Add candidate's response to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Show loading indicator while processing
        with st.spinner("Analyzing your response..."):
            # Evaluate the answer satisfaction
            evaluation = evaluate_answer_satisfaction(prompt, st.session_state.current_question)
            
            # Analyze the candidate's response
            analysis = analyze_candidate_response(prompt, st.session_state.current_question)
            
            # Generate a relevant follow-up question based on the response
            follow_up = generate_follow_up_question(
                prompt,
                {
                    "tech_stack": st.session_state.candidate_info["tech_stack"],
                    "current_question": st.session_state.current_question,
                    "current_topic": st.session_state.current_topic
                },
                is_satisfactory=evaluation["is_satisfactory"]
            )
            
            # Update chat with analysis and follow-up question
            feedback_message = f"""**Analysis of your response:**
{analysis['analysis']}

**Evaluation:**
- Score: {evaluation['score']}/10
- Feedback: {evaluation['feedback']}

**Next Question:**
{follow_up}"""

            st.session_state.messages.append({
                "role": "assistant",
                "content": feedback_message
            })
            
            # Update current question and increment counter
            st.session_state.current_question = follow_up
            st.session_state.questions_asked += 1
            
            # Update current topic if the answer was satisfactory
            if evaluation["is_satisfactory"]:
                st.session_state.current_topic = follow_up.split(']')[0].strip('[') if ']' in follow_up else "General"
            
            st.rerun()

# Display interview summary if available
if st.session_state.show_summary and st.session_state.interview_summary:
    st.markdown("### 📊 Interview Summary")
    st.markdown(st.session_state.interview_summary)
    
    # Add download button for the summary
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"interview_summary_{st.session_state.candidate_info['full_name'].replace(' ', '_')}_{timestamp}.txt"
    
    st.download_button(
        label="Download Interview Summary",
        data=st.session_state.interview_summary,
        file_name=filename,
        mime="text/plain"
    )
    
    # Add button to start new interview
    if st.button("Start New Interview"):
        # Reset all session state variables for a new interview
        st.session_state.interview_stage = "initial"
        st.session_state.messages = []
        st.session_state.current_question = None
        st.session_state.candidate_info = None
        st.session_state.greeting_sent = False
        st.session_state.questions_asked = 0
        st.session_state.current_topic = None
        st.session_state.is_processing = False
        st.session_state.interview_summary = None
        st.session_state.show_summary = False
        st.rerun()
