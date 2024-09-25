import os
from dotenv import load_dotenv

def load_environment():
    load_dotenv()
    google_headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": os.getenv("GOOGLE_API_HOST"),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    fast_translate_headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": os.getenv("FAST_API_HOST"),
        "Content-Type": "application/json"
    }

    return google_headers, fast_translate_headers
