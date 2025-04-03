"""
Utility functions for the TalentScout technical interview assistant.

This module provides core functionality for:
- Managing Hugging Face API interactions
- Generating technical interview questions
- Analyzing candidate responses
- Validating candidate information
- Generating follow-up questions

The module uses the Mistral-7B-Instruct-v0.2 model from Hugging Face for
AI-powered question generation and response analysis.
"""

import os
from typing import List, Dict, Any
import requests
from dotenv import load_dotenv
from datetime import datetime
from huggingface_hub import InferenceClient

# Load environment variables from .env file
load_dotenv()

def get_huggingface_client():
    """
    Initialize and return Hugging Face client.
    
    This function creates a new InferenceClient instance using the API key
    from environment variables. It is used for all AI-powered operations
    in the application.
    
    Returns:
        InferenceClient: Initialized Hugging Face client
        
    Raises:
        ValueError: If HUGGINGFACE_API_KEY is not set in environment variables
    """
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        raise ValueError(
            "HUGGINGFACE_API_KEY not found in environment variables. "
            "Please set it in your .env file."
        )
    return InferenceClient(token=api_key)

# Initialize Hugging Face client globally
try:
    client = get_huggingface_client()
except ValueError as e:
    print(f"Error: {e}")
    print("Please set your Hugging Face API key in the .env file")
    client = None

def make_api_request(messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 500) -> str:
    """
    Make a request to the Hugging Face API for text generation.
    
    This function formats the conversation messages into a prompt and sends
    it to the Mistral-7B-Instruct-v0.2 model for processing.
    
    Args:
        messages (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content' keys
        temperature (float): Controls randomness in the response (0.0 to 1.0)
        max_tokens (int): Maximum number of tokens in the generated response
        
    Returns:
        str: Generated response text from the model
        
    Raises:
        ValueError: If Hugging Face client is not initialized
    """
    if not client:
        raise ValueError("Hugging Face client not initialized. Please check your API key.")
    
    # Convert messages to prompt format using Mistral's instruction format
    prompt = "<s>[INST] "
    for message in messages:
        if message["role"] == "system":
            prompt += f"System: {message['content']}\n"
        elif message["role"] == "user":
            prompt += f"Human: {message['content']}\n"
        elif message["role"] == "assistant":
            prompt += f"Assistant: {message['content']}\n"
    prompt += " [/INST]"
    
    # Make the API request with optimized parameters
    response = client.text_generation(
        prompt,
        model="mistralai/Mistral-7B-Instruct-v0.2",
        max_new_tokens=max_tokens,
        temperature=temperature,
        top_p=0.95,  # Nucleus sampling parameter
        repetition_penalty=1.15  # Penalty for repeating tokens
    )
    
    return response

def evaluate_answer_satisfaction(response: str, question: str) -> Dict[str, Any]:
    """
    Evaluate if the candidate's answer is satisfactory.
    
    Args:
        response (str): The candidate's response
        question (str): The technical question asked
        
    Returns:
        Dict[str, Any]: Evaluation results including:
            - is_satisfactory (bool): Whether the answer is satisfactory
            - feedback (str): Detailed feedback
    """
    prompt = f"""Evaluate the candidate's response to the technical question:
    Question: {question}
    Response: {response}
    
    Provide a structured evaluation including:
    1. Technical accuracy (0-10)
    2. Completeness of the answer
    3. Clarity of explanation
    4. Whether the answer is satisfactory (true/false)
    
    Format the response as:
    Score: [number]
    Satisfactory: [true/false]
    Feedback: [detailed feedback]"""
    
    messages = [
        {"role": "system", "content": "You are an expert technical interviewer evaluating candidate responses."},
        {"role": "user", "content": prompt}
    ]
    
    evaluation = make_api_request(messages, temperature=0.3)
    
    # Parse the evaluation response
    lines = evaluation.split('\n')
    score = 0
    is_satisfactory = False
    feedback = ""
    
    for line in lines:
        if line.startswith("Score:"):
            try:
                score = int(line.split(":")[1].strip())
            except:
                pass
        elif line.startswith("Satisfactory:"):
            is_satisfactory = line.split(":")[1].strip().lower() == "true"
        elif line.startswith("Feedback:"):
            feedback = line.split(":")[1].strip()
    
    return {
        "is_satisfactory": is_satisfactory,
        "score": score,
        "feedback": feedback
    }

def generate_technical_questions(tech_stack: List[str], experience: int) -> List[str]:
    """
    Generate technical questions based on the candidate's tech stack and experience level.
    
    This function creates a balanced set of technical questions that:
    - Match the candidate's experience level (junior/mid-level/senior)
    - Cover all specified technologies
    - Include both theoretical and practical questions
    - Progress in difficulty based on experience
    
    Args:
        tech_stack (List[str]): List of technologies the candidate is familiar with
        experience (int): Years of experience of the candidate
        
    Returns:
        List[str]: List of technical questions tailored to the candidate
        
    Raises:
        ValueError: If Hugging Face client is not properly initialized
    """
    # Determine experience level and question parameters
    if experience < 2:
        level = "junior"
        question_count = 3
        complexity = "basic to intermediate"
    elif experience < 5:
        level = "mid-level"
        question_count = 4
        complexity = "intermediate to advanced"
    else:
        level = "senior"
        question_count = 5
        complexity = "advanced to expert"
    
    # Create a balanced prompt that ensures questions from all tech stacks
    tech_stack_str = ', '.join(tech_stack)
    prompt = f"""Generate {question_count} technical interview questions for a {level} developer with {experience} years of experience.
    The candidate is familiar with: {tech_stack_str}
    
    Requirements:
    1. Questions should be {complexity} level
    2. Include at least one question from each technology mentioned
    3. Mix of theoretical and practical questions
    4. Questions should test both knowledge and problem-solving abilities
    5. Include at least one system design or architecture question for {level} level
    6. Format each question as a clear, concise string
    
    Example format:
    1. [Technology] Question about specific concept
    2. [Technology] Practical problem-solving scenario
    3. [Technology] System design or architecture question
    """
    
    messages = [
        {"role": "system", "content": "You are a technical interviewer generating relevant interview questions based on experience level and tech stack."},
        {"role": "user", "content": prompt}
    ]
    
    response = make_api_request(messages, temperature=0.7)
    questions = response.split('\n')
    return [q.strip() for q in questions if q.strip()]

def analyze_candidate_response(response: str, question: str) -> Dict[str, Any]:
    """
    Analyze the candidate's response to a technical question.
    
    This function evaluates the candidate's response based on:
    - Technical accuracy
    - Clarity of explanation
    - Depth of understanding
    - Areas for improvement
    
    Args:
        response (str): The candidate's response text
        question (str): The technical question that was asked
        
    Returns:
        Dict[str, Any]: Analysis results including:
            - analysis: Detailed feedback and assessment
            - timestamp: ISO format timestamp of the analysis
            
    Raises:
        ValueError: If Hugging Face client is not properly initialized
    """
    prompt = f"""Analyze the following candidate response to the technical question:
    Question: {question}
    Response: {response}
    
    Provide a detailed analysis including:
    1. Technical accuracy (0-10)
    2. Clarity of explanation
    3. Areas for improvement
    4. Overall assessment
    
    Format the response as a structured analysis."""
    
    messages = [
        {"role": "system", "content": "You are an expert technical interviewer analyzing candidate responses."},
        {"role": "user", "content": prompt}
    ]
    
    analysis = make_api_request(messages, temperature=0.3)  # Lower temperature for more consistent analysis
    
    return {
        "analysis": analysis,
        "timestamp": datetime.now().isoformat()
    }

def generate_follow_up_question(previous_response: str, context: Dict[str, Any], is_satisfactory: bool = False) -> str:
    """
    Generate a follow-up question based on the candidate's previous response.
    
    This function creates a relevant follow-up question that:
    - Builds upon the candidate's previous answer if not satisfactory
    - Moves to a new topic if the previous answer was satisfactory
    
    Args:
        previous_response (str): The candidate's previous response
        context (Dict[str, Any]): Conversation context including tech stack and previous questions
        is_satisfactory (bool): Whether the previous answer was satisfactory
        
    Returns:
        str: A relevant follow-up question
        
    Raises:
        ValueError: If Hugging Face client is not properly initialized
    """
    if is_satisfactory:
        # Generate a new question from a different topic
        tech_stack = context.get("tech_stack", [])
        prompt = f"""Generate a new technical question from a different topic.
        The candidate is familiar with: {', '.join(tech_stack)}
        
        Requirements:
        1. Choose a different topic than the previous question
        2. Match the candidate's experience level
        3. Test a different aspect of their knowledge
        4. Format as a clear, concise question
        
        Previous question was about: {context.get('current_question', '')}
        """
    else:
        # Generate a follow-up question to explore the current topic further
        prompt = f"""Based on the candidate's previous response, generate a follow-up question to explore the topic further:
        Previous Response: {previous_response}
        Context: {context}
        
        Generate a focused, relevant follow-up question that builds upon the previous response."""
    
    messages = [
        {"role": "system", "content": "You are an expert technical interviewer generating follow-up questions."},
        {"role": "user", "content": prompt}
    ]
    
    return make_api_request(messages, temperature=0.7, max_tokens=200).strip()

def validate_candidate_info(info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and format candidate information.
    
    This function performs comprehensive validation of candidate information:
    - Checks for required fields
    - Validates email format
    - Validates phone number format
    - Formats and normalizes input data
    
    Args:
        info (Dict[str, Any]): Raw candidate information dictionary
        
    Returns:
        Dict[str, Any]: Validated and formatted information
        
    Raises:
        ValueError: If any mandatory field is missing or invalid
    """
    # Define mandatory fields and their display names
    mandatory_fields = {
        "full_name": "Full Name",
        "email": "Email",
        "phone": "Phone",
        "position": "Position Applied For",
        "tech_stack": "Tech Stack"
    }
    
    # Check for missing mandatory fields
    missing_fields = []
    for field, display_name in mandatory_fields.items():
        if not info.get(field, "").strip():
            missing_fields.append(display_name)
    
    if missing_fields:
        raise ValueError(f"Please fill in all mandatory fields: {', '.join(missing_fields)}")
    
    # Validate email format
    email = info.get("email", "").strip().lower()
    if not "@" in email or not "." in email:
        raise ValueError("Please enter a valid email address")
    
    # Validate phone number format (basic check)
    phone = info.get("phone", "").strip()
    if not phone.replace("-", "").replace("+", "").replace(" ", "").isdigit():
        raise ValueError("Please enter a valid phone number")
    
    # Validate and format tech stack
    tech_stack = [tech.strip() for tech in info.get("tech_stack", "").split(",") if tech.strip()]
    if not tech_stack:
        raise ValueError("Please enter at least one technology in the tech stack")
    
    # Create validated and formatted info dictionary
    validated_info = {
        "full_name": info.get("full_name", "").strip(),
        "email": email,
        "phone": phone,
        "experience": int(info.get("experience", 0)),
        "position": info.get("position", "").strip(),
        "location": info.get("location", "").strip(),
        "tech_stack": tech_stack
    }
    
    return validated_info 