from agents import Agent , Runner
import asyncio
from openai_study_mode_clone.agents_services.study_agent import study_agent
from openai_study_mode_clone.config.llm_model_config import model

async def base_agent(user_input: str) -> str:
    base_agent : Agent = Agent(
        name="Base Agent",
        instructions="You are a helpful assistant. You'r task is to understand the user's query and handoff to the appropriate specialized agent",
        model=model,
        handoffs=[study_agent],

    )
    response = await Runner.run(starting_agent=base_agent, input=user_input)
    # print(response.last_agent)
    return response.final_output

if __name__ == "__main__":
    user_input = "I need help with my math homework"
    response = asyncio.run(base_agent(user_input))
    print(response)