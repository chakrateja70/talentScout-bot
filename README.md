# TalentScout - AI-Powered Technical Interview Assistant

## Project Overview
TalentScout is an intelligent chatbot designed to streamline the technical interview process. It leverages the power of AI to conduct initial candidate screenings, gather information, and assess technical proficiency. The chatbot provides a structured, consistent, and efficient way to evaluate candidates while offering real-time feedback and analysis.

### Key Features
- 🤖 Automated candidate information gathering
- 📝 Experience-based technical question generation
- 🔍 Real-time response analysis
- 💬 Interactive follow-up questions
- 📊 Structured feedback system
- 🎯 Tech stack-specific assessments
- 👋 Personalized interview experience

## Installation Instructions

### Prerequisites
- Python 3.10 or higher
- Hugging Face API key
- Virtual environment (recommended)

### Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/chakrateja70/talentScout-bot
   cd talentscout
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

4. Create a `.env` file in the project root:
   ```
   HUGGINGFACE_API_KEY=your_api_key_here
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage Guide

### Starting an Interview
1. Fill in the candidate information in the sidebar:
   - Full Name
   - Email
   - Phone
   - Years of Experience
   - Position Applied For
   - Location
   - Tech Stack (comma-separated)

2. Click "Start Interview" to begin

### During the Interview
- Respond to technical questions in the chat interface
- Receive real-time feedback on your responses
- Answer follow-up questions to demonstrate your knowledge
- End the interview at any time by:
  - Clicking the "End Interview" button
  - Typing "exit", "quit", or "end interview"

## Technical Details

### Libraries Used
- `streamlit==1.32.0`: Web application framework
- `deepseek-ai==0.1.0`: AI model integration
- `python-dotenv==1.0.1`: Environment variable management
- `httpx==0.25.2`: HTTP client
- `requests==2.31.0`: HTTP requests

### Model Details
- **Model**: Mistral-7B-Instruct-v0.2
- **Provider**: Hugging Face
- **Capabilities**: 
  - Natural language understanding
  - Context-aware responses
  - Technical knowledge assessment
  - Response analysis

### Architecture
- **Frontend**: Streamlit-based UI
- **Backend**: Python-based logic
- **AI Integration**: Hugging Face API
- **State Management**: Streamlit session state

## Prompt Design

### Information Gathering
- Structured prompts for candidate information validation
- Clear formatting requirements for input fields
- Error handling for invalid inputs

### Technical Questions
- Experience-based question generation
- Tech stack-specific content
- Progressive difficulty based on experience level
- Mix of theoretical and practical questions

### Response Analysis
- Structured analysis format
- Technical accuracy assessment
- Areas for improvement identification
- Follow-up question generation

## Challenges & Solutions

### Challenge 1: Dynamic Question Generation
**Problem**: Generating relevant questions based on varying experience levels and tech stacks.

**Solution**: 
- Implemented experience-based categorization and tech stack-specific question templates
- Created difficulty levels (junior, mid-level, senior) with appropriate question counts
- Ensured balanced coverage of all specified technologies

### Challenge 2: Response Analysis
**Problem**: Providing meaningful feedback on technical responses.

**Solution**: 
- Created structured analysis prompts that evaluate multiple aspects of the response
- Implemented scoring system for technical accuracy
- Added specific feedback for areas of improvement
- Generated context-aware follow-up questions

### Challenge 3: State Management
**Problem**: Maintaining conversation context and interview progress.

**Solution**: 
- Utilized Streamlit's session state for persistent data management
- Implemented proper state initialization and cleanup
- Added state tracking for interview stages and messages
- Created robust error handling for state transitions

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Hugging Face for providing the AI model
- Streamlit team for the excellent framework
- All contributors and users of the project

## Support
For support, please open an issue in the GitHub repository or contact the maintainers. 
