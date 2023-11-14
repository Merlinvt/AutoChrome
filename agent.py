import autogen

from typing import Any, Dict, List, Optional

import time

import time
from io import BytesIO

from PIL import Image
from playwright.sync_api import sync_playwright
from vimbot import Vimbot
from vision import get_actions

vimium_path = "./vimium-master"

class AutoChromeAgent(autogen.AssistantAgent):

    def __init__(
        self,
        **kwargs,
    ):

        super().__init__(
            **kwargs,
        )
        self.objective = ""

        self.driver = Vimbot()

        print("Navigating to Google...")
        self.driver.navigate("https://www.google.com")


    def next_action()
        time.sleep(1)
        print("Capturing the screen...")
        creenshot = self.driver.capture()
        print("Getting actions for the given objective...")
        action = vision.get_actions(screenshot, objective)
        print(f"JSON Response: {action}")
        if self.driver.perform_action(action):  # returns True if done
            return "done with the task"
        


    def next(self, action):
        if "done" in action:
            return True
        if "click" in action and "type" in action:
            self.click(action["click"])
            self.type(action["type"])
        if "navigate" in action:
            self.navigate(action["navigate"])
        elif "type" in action:
            self.type(action["type"])
        elif "click" in action:
            self.click(action["click"])
    
    def get_actions(screenshot, objective):
        encoded_screenshot = encode_and_resize(screenshot)
        response = openai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"You need to choose which action to take to help a user do this task: {objective}. \
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
                                "url": f"data:image/jpeg;base64,{encoded_screenshot}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=100,
        )

        try:
            json_response = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            print("Error: Invalid JSON response")
            cleaned_response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant to fix an invalid JSON response. \
                        You need to fix the invalid JSON response to be valid JSON. \
                        You must respond in JSON only with no other fluff or bad things will happen. \
                    Do not return the JSON inside a code block."},
                    {"role": "user", "content": f"The invalid JSON response is: {response.choices[0].message.content}"}
                ]
            )
            try: cleaned_json_response = json.loads(cleaned_response.choices[0].message.content)
            except json.JSONDecodeError:
                print("Error: Invalid JSON response")
                return {}
            return cleaned_json_response

        return json_response


    def navigate(self, url):
        self.page.goto(url=url if "://" in url else "https://" + url, timeout=60000)

    def type(self, text):
        time.sleep(1)
        self.page.keyboard.type(text)
        self.page.keyboard.press("Enter")

    def click(self, text):
        self.page.keyboard.type(text)

    def capture(self):
        # capture a screenshot with vim bindings on the screen
        self.page.keyboard.press("Escape")
        self.page.keyboard.type("f")

        screenshot = Image.open(BytesIO(self.page.screenshot())).convert("RGB")
        return screenshot

def encode_and_resize(image):
    W, H = image.size
    image = image.resize((IMG_RES, int(IMG_RES * H / W)))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded_image

