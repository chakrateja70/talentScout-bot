# TalentScout - AI-Powered Technical Interview Assistant

## Project Overview

TalentScout is an intelligent technical interview assistant that leverages AI to conduct and analyze technical interviews. It provides a seamless experience for both interviewers and candidates by:

- Automatically generating relevant technical questions based on candidate experience and tech stack
- Evaluating candidate responses in real-time
- Providing detailed feedback and analysis
- Maintaining a structured interview flow
- Generating comprehensive interview summaries

## Features

### For Interviewers
- Automated technical assessment
- Smart question flow based on candidate responses
- Real-time response analysis and scoring
- Comprehensive feedback generation
- Downloadable interview summaries

### For Candidates
- Interactive interview experience
- Clear, structured questions
- Immediate feedback on responses
- Progress tracking
- Professional interview environment

## Installation Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/talentscout-bot.git
   cd talentscout-bot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your Hugging Face API key:
     ```
     HUGGINGFACE_API_KEY=your_api_key_here
     ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage Guide

1. **Starting the Interview**
   - Launch the application
   - Fill in candidate information in the sidebar
   - Click "Start Interview"

2. **During the Interview**
   - The system will generate relevant technical questions
   - Candidates can type their responses
   - Real-time analysis and feedback will be provided
   - Follow-up questions will be generated based on responses

3. **Ending the Interview**
   - Click "End Interview" when finished
   - Review the comprehensive interview summary
   - Download the summary for record-keeping

## Technical Details

### Libraries Used
- Streamlit (1.32.0+) - Web interface and UI components
- Hugging Face Hub (0.20.3+) - AI model integration
- Python-dotenv (1.0.1) - Environment variable management
- Requests (2.32.3+) - HTTP requests handling
- Python-dateutil (2.9.0+) - Date and time utilities
- Typing-extensions (4.12.2+) - Type hinting support

### AI Model
- Model: Mistral-7B-Instruct-v0.2
- Provider: Hugging Face
- Capabilities:
  - Question generation
  - Response analysis
  - Feedback generation
  - Summary creation

### Architecture
- Frontend: Streamlit-based web interface
- Backend: Python-based processing
- AI Integration: Hugging Face API
- State Management: Streamlit session state
- Data Flow: Real-time processing and feedback

## Prompt Design

### 1. Question Generation
```python
prompt = f"""Generate {question_count} technical interview questions for a {level} developer with {experience} years of experience.
The candidate is familiar with: {tech_stack_str}

Requirements:
1. Questions should be {complexity} level
2. Include at least one question from each technology
3. Mix of theoretical and practical questions
4. Questions should test both knowledge and problem-solving
5. Include system design questions for {level} level
"""
```

### 2. Response Analysis
```python
prompt = f"""Analyze the following candidate response:
Question: {question}
Response: {response}

Provide analysis including:
1. Technical accuracy (0-10)
2. Clarity of explanation
3. Areas for improvement
4. Overall assessment
"""
```

### 3. Follow-up Questions
```python
prompt = f"""Based on the candidate's response:
Question: {question}
Response: {response}
Previous questions: {previous_questions}

Generate a follow-up question that:
1. Builds on the candidate's answer
2. Tests deeper understanding
3. Explores related concepts
"""
```

## Challenges & Solutions

### 1. Response Quality Assessment
**Challenge**: Accurately evaluating technical responses
**Solution**: Implemented structured evaluation criteria and scoring system

### 2. Question Flow Management
**Challenge**: Maintaining coherent interview progression
**Solution**: Developed topic tracking and dynamic question generation

### 3. Real-time Processing
**Challenge**: Handling API latency during interviews
**Solution**: Implemented loading indicators and optimized API calls

### 4. State Management
**Challenge**: Maintaining interview context across sessions
**Solution**: Utilized Streamlit's session state for persistent data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hugging Face for providing the AI model
- Streamlit for the web framework
- All contributors who have helped improve the project