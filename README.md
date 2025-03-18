# TalentScout - AI-Powered Technical Interview Assistant

TalentScout is an intelligent technical interview assistant built with Streamlit and powered by Hugging Face's Mistral AI model. It helps streamline the initial screening process by conducting technical interviews, analyzing candidate responses, and providing structured feedback.

## Features

- 🤖 AI-powered technical interview questions generation
- 📝 Real-time response analysis and feedback
- 🔄 Dynamic follow-up questions based on candidate responses
- 📊 Structured candidate information gathering
- 💻 Clean and intuitive user interface
- 🔒 Secure API key management

## Prerequisites

- Python 3.10 or higher
- Virtual environment (recommended)
- Hugging Face API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/talentscout.git
cd talentscout
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root directory and add your Hugging Face API key:
```
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

To get a Hugging Face API key:
1. Go to [Hugging Face](https://huggingface.co/)
2. Create an account or sign in
3. Go to your profile settings
4. Navigate to "Access Tokens"
5. Create a new token with read access

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Follow the interview process:
   - Enter candidate information in the sidebar
   - Click "Start Interview" to begin
   - Answer the technical questions
   - Receive real-time feedback and follow-up questions
   - End the interview when finished

## Project Structure

```
talentscout/
├── app.py              # Main Streamlit application
├── utils.py            # Utility functions and API integration
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this file)
└── README.md          # Project documentation
```

## Technical Details

- **Frontend**: Streamlit
- **AI Model**: Mistral-7B-Instruct-v0.2 (via Hugging Face API)
- **Dependencies**:
  - streamlit==1.32.0
  - python-dotenv==1.0.1
  - requests>=2.32.3
  - huggingface-hub>=0.20.3

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Hugging Face](https://huggingface.co/) for providing access to the Mistral AI model
- [Mistral AI](https://mistral.ai/) for developing the powerful language model

## Support

If you encounter any issues or have questions, please open an issue in the GitHub repository. # talentScout-bot
