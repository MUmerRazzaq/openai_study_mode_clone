from agents import AsyncOpenAI , OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os

load_dotenv()


client : AsyncOpenAI = AsyncOpenAI(api_key=os.environ["GEMINI_API_KEY"], base_url=os.environ.get("LLM_CHAT_COMPLETION_URL"))
model : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(openai_client=client, model=os.environ.get("LLM_MODEL", "gemini-2.0-flash"))


