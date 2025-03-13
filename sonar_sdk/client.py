from openai import OpenAI
from dotenv import load_dotenv
import os

_client = None 

def get_client():
    global _client
    if _client is None:
        load_dotenv() 
        API_KEY = os.getenv("PLEX_API_KEY")
        if API_KEY is None:
            raise ValueError("PLEX_API_KEY is not set")
        _client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")
    return _client

