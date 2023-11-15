import autogen
from autogen import UserProxyAgent
import os

from agent import BrowsingAgent
from functions import functions_cfg

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
    "functions": functions_cfg,
    "config_list": config_list,
    "timeout": 120,
}

autogen.ChatCompletion.start_logging()
chatbot = BrowsingAgent(
    name="chatbot",
    system_message="You need to choose which action to take to help a user do this task: {objective}. \
        Your options are navigate, type, click, and done. Navigate should take you to the specified URL. \
        Type and click take strings where if you want to click on an object, \
        return the string with the yellow character sequence you want to click on, \
        and to type just a string with the message you want to type. \
        For clicks, please only respond with the 1-2 letter sequence in the yellow box, \
        and if there are multiple valid options choose the one you think a user would select. \
        For typing, please return a click to click on the box along with a type with the message to write. \
        When the page seems satisfactory, return done as a key with no value. \
        You must respond in JSON only with no other fluff or bad things will happen. \
        The JSON keys must ONLY be one of navigate, type, or click. Do not return the JSON inside a code block.",

    llm_config=llm_config,
)


#chatbot.register_function(
#    function_map={
#        "next_action": chatbot.next_action,
#    }
#)

user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding"},
)

autogen.oai.Completion(model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"You need to choose which action to take to help a user do this task: . \
                        Your options are navigate, type, click, and done. Navigate should take you to the specified URL. \
                        Type and click take strings where if you want to click on an object, \
                        return the string with the yellow character sequence you want to click on, \
                        and to type just a string with the message you want to type. For clicks, \
                        please only respond with the 1-2 letter sequence in the yellow box, \
                        and if there are multiple valid options choose the one you think a user would select. \
                        For typing, please return a click to click on the box along with a type with the message to write. \
                        When the page seems satisfactory, return done as a key with no value. \
                        You must respond in JSON only with no other fluff or bad things will happen. \
                        The JSON keys must ONLY be one of navigate, type, or click. Do not return the JSON inside a code block.",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,",
                    },
                },
            ],
        }
    ],
)
chatbot.next_action()
#user_proxy.initiate_chat(
#    chatbot,
#    message="go to zeit.de and click the first article"
#)
