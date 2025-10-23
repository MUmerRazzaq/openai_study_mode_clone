# Use official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Ensure predefined Chainlit config, translations, and UI assets are used
# Copy project-level .chainlit (if present under src) to root so Chainlit picks it up
RUN if [ -d "/app/src/openai_study_mode_clone/.chainlit" ]; then \
            mkdir -p /app/.chainlit && cp -r /app/src/openai_study_mode_clone/.chainlit/* /app/.chainlit/ ; \
        fi && \
    echo "Checking .chainlit config..." && \
    ls -la /app/.chainlit/ || echo "WARNING: No .chainlit directory found!"
    
# Copy custom chainlit.md to root if provided in src
RUN if [ -f "/app/src/openai_study_mode_clone/chainlit.md" ]; then \
            cp /app/src/openai_study_mode_clone/chainlit.md /app/chainlit.md ; \
        fi && \
    ls -la /app/chainlit.md || echo "WARNING: No chainlit.md found!"
    
# Copy public assets to root so /public/* URLs work
RUN if [ -d "/app/src/openai_study_mode_clone/public" ]; then \
            cp -r /app/src/openai_study_mode_clone/public /app/public ; \
        fi && \
    ls -la /app/public/ || echo "WARNING: No public directory found!"

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install chainlit openai-agents websockets

# Install the project package
RUN pip install -e .

# Create directory for SQLite databases (persistent storage)
RUN mkdir -p /app/data && chmod 777 /app/data

# Expose Chainlit default port
EXPOSE 7860

# Set environment variable for OpenAI API key (override at runtime)
# ENV OPENAI_API_KEY=your-key-here

# Trust reverse proxy headers (needed on Hugging Face Spaces)
ENV FORWARDED_ALLOW_IPS="*"

# Set Chainlit URL for WebSocket connections (will be overridden by Space secrets if set)
ENV CHAINLIT_URL="https://mumerrazzaq-studybuddy.hf.space"

# Start Chainlit app for Hugging Face Spaces reverse proxy
CMD ["chainlit", "run", "src/openai_study_mode_clone/app.py", "--host", "0.0.0.0", "--port", "7860"]