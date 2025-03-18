"""
Initiates and runs Survey Agents
"""
import os

from dotenv import load_dotenv
from src.agents import SurveyAgent

load_dotenv()


if __name__ == '__main__':
    agent = SurveyAgent(login_url = os.getenv("LOGIN_URL"))