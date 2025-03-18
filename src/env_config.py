"""
File to load all configuration variables for rest of the application
"""
import os

from dotenv import load_dotenv
load_dotenv()

LOGIN_URL = os.getenv("LOGIN_URL")
