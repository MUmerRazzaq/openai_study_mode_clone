---
title: Study Mode
emoji: 📚
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
short_description: AI-Powered Study Assistant built with Chainlit and OpenAI
tags:
  - education
  - chatbot
  - ai-assistant
  - study
  - learning
---

# Study Mode – AI-Powered Study Assistant

**Study Mode** is an interactive AI assistant built with Chainlit and OpenAI, designed to help students learn, review, and practice more effectively.

## Features

- **Homework Help:** Get step-by-step guidance and concept explanations.
- **Exam Review:** Request study plans, topic breakdowns, and practice questions.
- **Concept Mastery:** Receive clear explanations, examples, and mini-quizzes.
- **Study Planning:** Build daily or weekly routines tailored to your goals.
- **Conversational Learning:** The assistant guides you with questions, hints, and feedback—never just giving answers.

## How to Use

1. **Start the app:**  
   Run the following command in your project directory:
   ```
   chainlit run src/openai_study_mode_clone/app.py
   ```
2. **Open in browser:**  
   Visit [http://localhost:7860](http://localhost:7860) to chat with your Study Assistant.
3. **Choose a starter or ask a question:**  
   Select a starter (e.g., “Help Me Study for My Exam”) or type your own question to begin.

## Project Structure

- `src/openai_study_mode_clone/agents_services/` – Agent logic and streaming service
- `src/openai_study_mode_clone/config/` – Model configuration
- `src/openai_study_mode_clone/prompts/` – Prompt templates
- `chainlit.md` – Custom welcome screen
- `README.md` – Project info and setup

## Requirements

- Python 3.10+
- [Chainlit](https://docs.chainlit.io)
- Gemini API key (for LLM)

## Setup

### Local Development

1. Install dependencies:
   ```
   pip install chainlit openai-agents
   ```
2. Set your API keys in `.env`:
   ```
   GEMINI_API_KEY=your-gemini-api-key
   LLM_CHAT_COMPLETION_URL=https://generativelanguage.googleapis.com/v1beta/openai/
   LLM_MODEL=gemini-2.0-flash
   ```
3. Run the app:
   ```
   chainlit run src/openai_study_mode_clone/app.py
   ```

### Hugging Face Spaces Deployment

See [HUGGINGFACE_SETUP.md](./HUGGINGFACE_SETUP.md) for detailed deployment instructions and troubleshooting.

**Required Environment Variables:**

- `GEMINI_API_KEY` - Your Gemini API key
- `LLM_CHAT_COMPLETION_URL` - Usually `https://generativelanguage.googleapis.com/v1beta/openai/`

## License

MIT
