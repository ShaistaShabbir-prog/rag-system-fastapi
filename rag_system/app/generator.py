import openai
from app.config import config
from loguru import logger

openai.api_key = config.OPENAI_API_KEY

def generate_answer(context: str, query: str) -> str:
    """Generates an answer using OpenAI GPT with retrieved context."""
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
    
    logger.info("Generating response with OpenAI")
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()
