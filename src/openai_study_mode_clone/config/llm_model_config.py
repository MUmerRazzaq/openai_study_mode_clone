from agents import AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

def get_llm_client() -> AsyncOpenAI:
    """
    Initializes and returns the asynchronous LLM client.

    Raises:
        ValueError: If the required API key or base URL environment variables are not set.

    Returns:
        AsyncOpenAI: An instance of the async LLM client.
    """
    # The API key for the service. The variable name suggests a Gemini model provider
    # that uses an OpenAI-compatible API.
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    # The base URL for the chat completion endpoint.
    base_url = os.environ.get("LLM_CHAT_COMPLETION_URL")
    if not base_url:
        raise ValueError("LLM_CHAT_COMPLETION_URL environment variable not set.")

    return AsyncOpenAI(api_key=api_key, base_url=base_url)

def get_llm_model(client: AsyncOpenAI) -> OpenAIChatCompletionsModel:
    """
    Initializes and returns the chat completions model.

    Args:
        client (AsyncOpenAI): The client to use for the model.

    Returns:
        OpenAIChatCompletionsModel: An instance of the chat completions model.
    """
    model_name = os.environ.get("LLM_MODEL", "gemini-2.0-flash")
    return OpenAIChatCompletionsModel(openai_client=client, model=model_name)

# Create singleton instances to be imported by other modules
client: AsyncOpenAI = get_llm_client()
model: OpenAIChatCompletionsModel = get_llm_model(client)
