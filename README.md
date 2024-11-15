# Voicebot Project

Welcome to the Voicebot Project! This project leverages OpenAI as the language model, ElevenLabs for text-to-speech conversion, and Flask for the backend services. The goal is to create an intelligent voicebot capable of understanding and responding to user inputs.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This voicebot project integrates advanced AI capabilities to provide seamless, conversational interactions. By combining the power of OpenAI's language model with ElevenLabs' text-to-speech technology and Flask for backend processing, the bot can understand natural language queries and respond audibly.

## Features
- **Natural Language Processing (NLP)**: Uses OpenAI to understand and generate human-like responses.
- **Text-to-Speech (TTS)**: Converts text responses to speech using ElevenLabs.
- **Backend Services**: Built on Flask, providing a robust and scalable API.
- **Real-time Interaction**: Processes user queries and responds in real time.
- **Sentiment and Emotion Analysis**: Integrates `pysentimiento` for analyzing user sentiment and emotions in Spanish, enhancing interaction quality.

## Installation
To get started with the project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sowiroar/voicebotIA.git
   cd voicebotIA
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Ensure that your API keys for OpenAI and ElevenLabs are securely stored as environment variables.
   ```bash
   export OPENAI_API_KEY='your-openai-api-key'
   export ELEVENLABS_API_KEY='your-elevenlabs-api-key'
   ```
   On Windows:
   ```cmd
   set OPENAI_API_KEY=your-openai-api-key
   set ELEVENLABS_API_KEY=your-elevenlabs-api-key
   ```

## Usage
Run the Flask application to start the voicebot service:
```bash
flask run
```

Interact with the bot through the designated web interface or API endpoint. The voicebot will process input text, respond using OpenAI, and generate speech through ElevenLabs.

## Configuration
- **OpenAI**: Ensure your OpenAI API key is correctly configured and has sufficient usage limits.
- **ElevenLabs**: Set up your ElevenLabs API key for TTS functionality.
- **Flask**: Modify `config.py` for any custom Flask settings if needed.

## Contributing
We welcome contributions! Feel free to submit a pull request or open an issue.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add a new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---
Thank you for using the Voicebot Project. We hope it enhances your interactions and AI development experience!
