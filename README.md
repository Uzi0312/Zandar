Zandar is an advanced AI-driven personal assistant designed to perform a variety of tasks using natural language processing (NLP) and machine learning (ML) techniques. It leverages voice recognition, command execution, and automated responses to assist users with everyday tasks. The assistant is capable of executing system-level commands, managing applications, fetching information from the web, and learning from user interactions to improve its functionality over time.

Features
Voice Recognition: Accepts voice commands and responds accordingly.
Natural Language Processing: Uses NLP to understand and process user queries.
Command Execution: Executes system-level commands like opening and closing applications, controlling volume, and managing system settings.
Web Information Fetching: Searches the web for information and performs tasks like playing YouTube videos or fetching weather updates.
Learning Capability: Learns from user interactions to enhance its responses and functionality.
Automated Responses: Provides automated responses based on predefined queries and responses.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/zandar.git
cd zandar
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Download the necessary models:

python
Copy code
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
Usage
Ensure your microphone is connected and working.
Run the Zandar script:
bash
Copy code
python zandar.py
Follow the voice prompts to interact with Zandar.
Configuration
Chrome Driver Path: Set the path to your ChromeDriver executable.

python
Copy code
chromedriver = r"C:\path\to\chromedriver.exe"
Query Files: Ensure the paths to the query and response files are correctly set:

python
Copy code
basic_responses_path = r"C:\path\to\Basic Responses.txt"
queries_path = r"C:\path\to\Queries.txt"
tags_path = r"C:\path\to\Tags.txt"
Dependencies
Python 3.8+
Pyttsx3
SpeechRecognition
Cryptography
PyAutoGUI
Selenium
PyWhatKit
PyTube
Pyperclip
psutil
pyjokes
requests
SentenceTransformers
Spacy
Difflib
Shutil
Platform
Subprocess
Ctypes
