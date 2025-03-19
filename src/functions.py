"""
Functions to execute by agents
"""
import json

from src.env_config import API_KEY

from openai import OpenAI

def determine_presence_of_modal(page_source, 
                                model = 'gpt-4o'):
    """Determine if there is a modal being displayed and process its contents"""

    system_prompt = f"""
    You are an AI agent that is being used to test website activity with selenium.
    Your job is to study the source code of a web page and determine if there is a modal being displayed.
    If there is, determine XPATH selectors that could be used to exit out of the modal, as well as that of the primary button.
    Also determine the text on the primary button on the modal.  

    The selector you return should be able to be placed into the following code:

    modal_exit = self.driver.find_element(By.XPATH, 
                                YOUR_ANSWER_HERE)
    modal_exit.click()

    Return your code ONLY in JSON format.  Give your responses the following
    structure:

    \\{{
        "has_modal": bool, True if page has modal, False if not,
        "modal_button_text": str, the text that appears on the primary button, None if has_modal is False,
        "exit_selector": str, the XPATH selector to locate the modal exit button, None if has_modal is False,
        "button_selector": str, the XPATH selector to locate the primary button, None if has_modal is False
    \\}}

    Here is the source code for the page: 

    {page_source}
    """

    client = OpenAI(api_key=API_KEY)
    completion = client.chat.completions.create(
        model = model,
        messages = [{"role": "system", 
                     "content": system_prompt}],
        response_format={"type": "json_object"}
    )

    ai_analysis = json.loads(completion.choices[0].message.content)
    return ai_analysis