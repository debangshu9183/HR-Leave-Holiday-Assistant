import os
from groq import Groq

MODEL  = "llama-3.3-70b-versatile"

def create_client():
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=GROQ_API_KEY)
    return client