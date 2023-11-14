import autogen
from agent import AutoChromeAgent
import os

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


user_proxy = AutoChromeAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    #human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding"},
    debugger_address="9222"
)

user_proxy.initiate_chat(
    chatbot,
    message="open chrome with selenium on the debugging port 9222   \
    go to google.de, then go to zeit.de don't clone it", 
)
