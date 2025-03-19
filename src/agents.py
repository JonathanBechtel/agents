"""
Folder that holds base classes for the different AI agents
"""
import json
import time

from src.utils import function_to_schema, load_user_info
from src.env_config import API_KEY
from src.functions import determine_presence_of_modal

from openai import OpenAI

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class OpenAIAgent:
    """
    Base class for all AI agents
    """
    def __init__(self, 
                 system_prompt: dict,
                 model: str,
                 functions: list) -> None:
        self.openai = OpenAI(api_key=API_KEY)
        self.messages = []
        self.system_prompt = system_prompt
        self.model = model
        self.tool_schemas = [function_to_schema(func)
                            for func in functions]
        self.tool_map = {func.__name__: func for func in functions}

    def _run_full_turn(self, user_message: str):
        """
        Top to bottom execution of OpenAI API Call
        """
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        completion = self.openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "developer",
                    "content": self.system_prompt}] + [self.messages],
            tools=self.tools
        ).choices[0].message

        # if model returns response, process this
        if completion.content:
            self.messages.append({
                "role": "assistant",
                "content": completion.content
            })

            print(f"Assistant: {completion.content}")

        if completion.tool_calls:
            for tool_call in completion.tool_calls:
                result = self._execute_tool_call(tool_call)
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
      
    # if it executes a function call, run through all of them

    def _execute_tool_call(self, tool_call):
        name = tool_call.function.name
        args = json.loads(tool_call.function.args)

        # better way to put your own spin on this?
        return self.tools_map[name](**args)
    
    def run_agent(self):
        print("Beginning agent.  Type 'exit' to quit")

        while True:
            user_message = input()
            if user_message == 'exit':
                break
            self._run_full_turn(user_message)


class WebAutomationAgent:

    def __init__(self, login_url: str):

        self.login_url = login_url
        self.credentials = load_user_info()
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service = service)
        self.wait = WebDriverWait(self.driver, 10)


    def login(self):

        try:
            # go to login page
            self.driver.get(self.login_url)

            # get the fields for logging in
            username_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Email or Swag Name')]")))
            password_field = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Password')]")
            
            # enter credentials
            username_field.send_keys(self.credentials["username"])
            time.sleep(4)
            password_field.send_keys(self.credentials["password"])
            time.sleep(3)

            # login!
            login_button = self.driver.find_element(By.XPATH, 
                                "//button/span[contains(text(), 'Sign in')]")
            login_button.click()
            time.sleep(10)
            
            # Wait for dashboard to load
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body.loggedIn"))
            )

            print("Successfully logged in!")

            return True

        except Exception as e:
            print(f"Could not login because: {e}")

            return False
        
    def clear_modal(self):

        page_html = self.driver.find_element(By.TAG_NAME, "body").text
        modal_info = determine_presence_of_modal(page_html)
        print(modal_info)
        links_to_survey = 'survey' in modal_info['modal_button_text'].lower().strip() if modal_info["has_modal"] else False

        if modal_info["has_modal"] and links_to_survey:
            modal_button = self.driver.find_element(By.XPATH, modal_info["button_selector"])
            time.sleep(3)
            modal_button.click()
        if modal_info["has_modal"] and not links_to_survey:
            exit_button = self.driver.find_element(By.XPATH, modal_info["exit_selector"])
            time.sleep(3)
            exit_button.click()

class SurveyAgent:

    def __init__(self, login_url: str):

        self.login_url = login_url
        self.web_agent = WebAutomationAgent(login_url = login_url)

    def _login(self):

        self.logged_in_ = self.web_agent.login()


    def run(self):

        self._login()

        time.sleep(60)

        self.web_agent.clear_modal()










    

