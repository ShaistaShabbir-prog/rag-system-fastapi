# import openai
from app.config import config

# from loguru import logger

# openai.api_key = config.OPENAI_API_KEY


# def generate_answer(context: str, query: str) -> str:
#     """Generates an answer using OpenAI GPT with retrieved context."""
#     prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"

#     logger.info("Generating response with OpenAI")

#     try:
#         # Make the API request to OpenAI for the answer
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # You can use "gpt-4" or other models as well
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt},  # Combining context and query here
#             ],
#             max_tokens=100,
#         )
#         # Extract the generated answer from the response
#         answer = response["choices"][0]["message"]["content"]
#         return answer

#     except Exception as e:
#         logger.error(f"Error generating answer: {e}")
#         return "Sorry, I couldn't generate an answer at this time."
import os
from openai import OpenAI
from loguru import logger

# Ensure your API key is set correctly
api_key = os.environ.get("OPENAI_API_KEY")  # Or directly use your API key here

client = OpenAI(api_key=api_key)


def generate_answer(context: str, query: str) -> str:
    """Generates an answer using OpenAI GPT with retrieved context."""
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"

    logger.info(f"Generated prompt: {prompt}")

    try:
        # Making the API call using the new client format
        response = client.responses.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" or "" depending on your requirement
            instructions="You are a helpful assistant.",  # Example instructions
            input=prompt,  # The combined context and query
        )

        logger.info(f"OpenAI response: {response}")

        # Extracting the generated answer from the response
        answer = (
            response.output_text.strip()
        )  # Adjust for correct key based on response structure
        return answer

    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        return "Sorry, I couldn't generate an answer at this time."
