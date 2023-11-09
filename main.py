import autogen
import os
#from llm_config import selenium_functions
from functions import (
    initialize_webdriver,
    google_search,
    previous_webpage,
    describe_website,
    close_webdriver,
    click_button_by_text,
    find_form_inputs,
    scroll,
    exec_python,
    get_url
)

from utils import (
    LoggingWebDriver,
    LoggingActionChains
)

# Load the API key from an environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ValueError("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")

config_list = [
    {
        'model': 'gpt-4',
        "api_key": openai_api_key
    }
]

llm_config = {
    #"functions": selenium_functions,
    "config_list": config_list,
    "timeout": 120,
}

autogen.ChatCompletion.start_logging()
chatbot = autogen.AssistantAgent(
    name="chatbot",
    system_message="For coding tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
    llm_config=llm_config,
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    #human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding"},
)

def exec_sh(script):
    return user_proxy.execute_code_blocks([("sh", script)])

# register the functions
"""
user_proxy.register_function(
    function_map={
        "python": exec_python,
        "sh": exec_sh,
        # Webdriver functions
        "initialize_webdriver": initialize_webdriver,
        "google_search": google_search,
        "previous_webpage": previous_webpage,
        "describe_website": describe_website,
        "close_webdriver": close_webdriver,
        "click_button_by_text": click_button_by_text,
        "find_form_inputs": find_form_inputs,
        "scroll": scroll,
        "get_url": get_url
    }
)
"""

# start the conversation
user_proxy.initiate_chat(
    chatbot,
    message="open chrome with selenium on the debugging port 9222   \
go to google.de, then go to zeit.de", 
)

autogen.ChatCompletion.stop_logging()
autogen.ChatCompletion.print_usage_summary()
logged_history = autogen.ChatCompletion.logged_history
print(logged_history)