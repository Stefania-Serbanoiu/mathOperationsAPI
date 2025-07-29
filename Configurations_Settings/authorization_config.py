from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env file

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
