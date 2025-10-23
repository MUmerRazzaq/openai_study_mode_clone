from agents import AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

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
        logger.error("GEMINI_API_KEY environment variable not set.")
        logger.info("Available environment variables: " + ", ".join([k for k in os.environ.keys() if not k.lower().endswith('key')]))
        raise ValueError("GEMINI_API_KEY environment variable not set. Please add it to your Hugging Face Space secrets.")

    # The base URL for the chat completion endpoint.
    base_url = os.environ.get("LLM_CHAT_COMPLETION_URL")
    if not base_url:
        logger.error("LLM_CHAT_COMPLETION_URL environment variable not set.")
        logger.info("Available environment variables: " + ", ".join([k for k in os.environ.keys() if not k.lower().endswith('key')]))
        raise ValueError("LLM_CHAT_COMPLETION_URL environment variable not set. Please add it to your Hugging Face Space secrets.")

    logger.info(f"LLM client initialized with base_url: {base_url}")
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
    logger.info(f"LLM model initialized: {model_name}")
    return OpenAIChatCompletionsModel(openai_client=client, model=model_name)

# Create singleton instances to be imported by other modules
try:
    logger.info("=" * 50)
    logger.info("STARTUP: Initializing LLM client and model...")
    logger.info("=" * 50)
    client: AsyncOpenAI = get_llm_client()
    model: OpenAIChatCompletionsModel = get_llm_model(client)
    logger.info("=" * 50)
    logger.info("STARTUP: LLM client and model initialized successfully")
    logger.info("=" * 50)
except Exception as e:
    logger.error("=" * 50)
    logger.error(f"STARTUP FAILED: Failed to initialize LLM client/model: {str(e)}")
    logger.error("=" * 50)
    logger.error("This will cause the container to crash and restart.")
    logger.error("Please check your Hugging Face Space secrets and ensure:")
    logger.error("  1. GEMINI_API_KEY is set")
    logger.error("  2. LLM_CHAT_COMPLETION_URL is set")
    logger.error("  3. Optional: LLM_MODEL (defaults to gemini-2.0-flash)")
    raise
