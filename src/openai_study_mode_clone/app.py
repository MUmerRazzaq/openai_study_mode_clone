import chainlit as cl
import uuid
import logging
import traceback
import sys
import os
from openai_study_mode_clone.agents_services.study_agent import study_agent_service

# Configure logging with explicit stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

logger.info("=" * 50)
logger.info("CHAINLIT APP: Starting up...")
logger.info("=" * 50)

# Verify config files exist
import pathlib
config_path = pathlib.Path("/app/.chainlit/config.toml")
md_path = pathlib.Path("/app/chainlit.md")
public_path = pathlib.Path("/app/public")

logger.info(f"Config file exists: {config_path.exists()} at {config_path}")
logger.info(f"Chainlit.md exists: {md_path.exists()} at {md_path}")
logger.info(f"Public directory exists: {public_path.exists()} at {public_path}")

if config_path.exists():
    logger.info(f"Config file size: {config_path.stat().st_size} bytes")
else:
    logger.warning("⚠️ Chainlit config.toml NOT FOUND! UI may not work correctly.")

logger.info("=" * 50)

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Help Me Study for My Exam",
            message=(
                "I have an upcoming exam. Please help me review the key topics step-by-step. "
                "Start by asking which subject and topics I need help with, then create a short study plan."
            ),
            icon="/public/exam.webp",
        ),

        cl.Starter(
            label="Explain My Homework",
            message=(
                "I have a homework question I don’t fully understand. "
                "Guide me through it step-by-step instead of just giving the answer, "
                "and help me learn the concept behind it."
            ),
            icon="/public/homework.webp",
        ),

        cl.Starter(
            label="Understand a Difficult Concept",
            message=(
                "There’s a topic I’m struggling to understand. "
                "Ask me which topic it is, find out what I already know, and then explain it in a simple, clear way "
                "with examples and small questions."
            ),
            icon="/public/learn.webp",
        ),

        cl.Starter(
            label="Quick Quiz Practice",
            message=(
                "I want to test my understanding with a short quiz. "
                "Ask what subject or topic I want to practice, then give me one question at a time and explain after each one."
            ),
            icon="/public/quiz.png",
        ),

        cl.Starter(
            label="Study Routine or Plan",
            message=(
                "Help me create a daily or weekly study plan that fits my schedule and exam goals. "
                "Ask about my subjects, available time, and preferred learning style first."
            ),
            icon="/public/plan.png",
        ),
    ]


@cl.on_chat_start
async def main():
    try:
        user_id = str(uuid.uuid4())
        cl.user_session.set("user_id", user_id)
        logger.info(f"New chat session started with user_id: {user_id}")
    except Exception as e:
        logger.error(f"Error in chat start: {str(e)}")
        logger.error(traceback.format_exc())
        await cl.Message(content=f"⚠️ Failed to start chat session. Please refresh and try again. ERROR: {str(e)}").send()
    

@cl.on_message
async def handle_message(message: cl.Message):
    user_id = None
    msg = None
    try:
        user_id = cl.user_session.get("user_id")
        logger.info(f"Received message from user {user_id}: {message.content[:100]}...")
        
        # Use a visible placeholder to ensure the message card renders before streaming
        msg = cl.Message(content="...\n")
        await msg.send()
 
        chunk_count = 0
        async for chunk in study_agent_service(message.content, user_id):
            if chunk:
                msg.content += chunk
                await msg.send()
                chunk_count += 1
        
        # await msg.update()
        logger.info(f"Message processed successfully for user {user_id}. Streamed {chunk_count} chunks.")
        logger.info(f"Response preview: {msg.content[:200]}...")
        
    except Exception as e:
        error_msg = f"Error processing message for user {user_id}: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        if msg is not None:
            msg.content = f"\n\n⚠️ An error occurred while generating the response. Please try again. ERROR: {str(e)}"
            await msg.send()
        else:
            await cl.Message(content=f"⚠️ An error occurred while generating the response. Please try again. ERROR: {str(e)}").send()




@cl.on_chat_end
async def on_chat_end():
    user_id = cl.user_session.get("user_id")
    logger.info(f"Chat session ended for user {user_id}")


@cl.on_stop
async def on_stop():
    user_id = cl.user_session.get("user_id")
    logger.info(f"Message generation stopped by user {user_id}")