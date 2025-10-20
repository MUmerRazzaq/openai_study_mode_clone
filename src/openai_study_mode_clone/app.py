import chainlit as cl
from openai_study_mode_clone.agents_services.study_agent import study_agent_service


@cl.on_chat_start
async def main():
    cl.user_session.set("user_id", "user_123")  # Example user ID; replace with actual user identification logic
    await cl.Message(content="Hello! I'm your Study Assistant. How can I help you today?").send()

@cl.on_message
async def handle_message(message: str):
    user_id = cl.user_session.get("user_id")
    response = await study_agent_service(message.content, user_id)
    
    await cl.Message(content=response).send()