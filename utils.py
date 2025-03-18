import os
from typing import List, Dict, Any
import requests
from dotenv import load_dotenv
from datetime import datetime
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

def get_huggingface_client():
    """
    Initialize and return Hugging Face client.
    
    Returns:
        InferenceClient: Hugging Face client
        
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

# Initialize Hugging Face client
try:
    client = get_huggingface_client()
except ValueError as e:
    print(f"Error: {e}")
    print("Please set your Hugging Face API key in the .env file")
    client = None

def make_api_request(messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 500) -> str:
    """
    Make a request to the Hugging Face API.
    
    Args:
        messages (List[Dict[str, str]]): List of message dictionaries
        temperature (float): Temperature for response generation
        max_tokens (int): Maximum tokens in response
        
    Returns:
        str: Generated response text
    """
    if not client:
        raise ValueError("Hugging Face client not initialized. Please check your API key.")
    
    # Convert messages to prompt format
    prompt = "<s>[INST] "
    for message in messages:
        if message["role"] == "system":
            prompt += f"System: {message['content']}\n"
        elif message["role"] == "user":
            prompt += f"Human: {message['content']}\n"
        elif message["role"] == "assistant":
            prompt += f"Assistant: {message['content']}\n"
    prompt += " [/INST]"
    
    # Make the API request
    response = client.text_generation(
        prompt,
        model="mistralai/Mistral-7B-Instruct-v0.2",
        max_new_tokens=max_tokens,
        temperature=temperature,
        top_p=0.95,
        repetition_penalty=1.15
    )
    
    return response

def generate_technical_questions(tech_stack: List[str], experience: int) -> List[str]:
    """
    Generate technical questions based on the candidate's tech stack and experience level.
    
    Args:
        tech_stack (List[str]): List of technologies the candidate is familiar with
        experience (int): Years of experience of the candidate
        
    Returns:
        List[str]: List of technical questions
        
    Raises:
        ValueError: If Hugging Face client is not properly initialized
    """
    # Determine experience level
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
    
    Args:
        response (str): The candidate's response
        question (str): The technical question asked
        
    Returns:
        Dict[str, Any]: Analysis results including score and feedback
        
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
    
    analysis = make_api_request(messages, temperature=0.3)
    
    return {
        "analysis": analysis,
        "timestamp": datetime.now().isoformat()
    }

def generate_follow_up_question(previous_response: str, context: Dict[str, Any]) -> str:
    """
    Generate a follow-up question based on the candidate's previous response.
    
    Args:
        previous_response (str): The candidate's previous response
        context (Dict[str, Any]): Conversation context including tech stack and previous questions
        
    Returns:
        str: A relevant follow-up question
        
    Raises:
        ValueError: If Hugging Face client is not properly initialized
    """
    prompt = f"""Based on the candidate's previous response and context, generate a relevant follow-up question:
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
    
    Args:
        info (Dict[str, Any]): Raw candidate information
        
    Returns:
        Dict[str, Any]: Validated and formatted information
        
    Raises:
        ValueError: If any mandatory field is missing or invalid
    """
    # Check mandatory fields
    mandatory_fields = {
        "full_name": "Full Name",
        "email": "Email",
        "phone": "Phone",
        "position": "Position Applied For",
        "tech_stack": "Tech Stack"
    }
    
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
    
    # Validate phone number (basic check)
    phone = info.get("phone", "").strip()
    if not phone.replace("-", "").replace("+", "").replace(" ", "").isdigit():
        raise ValueError("Please enter a valid phone number")
    
    # Validate tech stack
    tech_stack = [tech.strip() for tech in info.get("tech_stack", "").split(",") if tech.strip()]
    if not tech_stack:
        raise ValueError("Please enter at least one technology in the tech stack")
    
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