"""
File to load all configuration variables for rest of the application
"""
import os

from dotenv import load_dotenv
load_dotenv()

LOGIN_URL = os.getenv("LOGIN_URL")
API_KEY = os.getenv("OPENAI_API_KEY")

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

