"""
Initiates and runs Survey Agents
"""

from src.agents import SurveyAgent
from src.env_config import LOGIN_URL


if __name__ == '__main__':
    agent = SurveyAgent(login_url = LOGIN_URL)
    agent.run()