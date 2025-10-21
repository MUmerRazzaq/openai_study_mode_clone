import chainlit as cl
import uuid
from openai_study_mode_clone.agents_services.study_agent import study_agent_service


@cl.on_chat_start
async def main():
    cl.user_session.set("user_id", str(uuid.uuid4()))  # Generate a unique user ID
    await cl.Message(content="Hello! I'm your Study Assistant. How can I help you today?").send()

@cl.on_message
async def handle_message(message: str):
    user_id = cl.user_session.get("user_id")
    msg = cl.Message(content="making progress...\n")
    await msg.send()

    async for chunk in study_agent_service(message.content, user_id):
        
        await msg.stream_token(chunk)
    
    await msg.send()