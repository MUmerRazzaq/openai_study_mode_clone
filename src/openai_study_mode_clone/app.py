import chainlit as cl
import uuid
from openai_study_mode_clone.agents_services.study_agent import study_agent_service

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
    cl.user_session.set("user_id", str(uuid.uuid4()))  # Generate a unique user ID
    # await cl.Message(content="Hello! I'm your Study Assistant. How can I help you today?").send()
    

@cl.on_message
async def handle_message(message: str):
    user_id = cl.user_session.get("user_id")
    msg = cl.Message(content="...\n")
    await msg.send()

    async for chunk in study_agent_service(message.content, user_id):
        
        await msg.stream_token(chunk)
    
    await msg.send()