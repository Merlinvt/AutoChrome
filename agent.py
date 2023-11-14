import autogen

from typing import Any, Dict, List, Optional

import time

import time
from io import BytesIO

from PIL import Image
from playwright.sync_api import sync_playwright

vimium_path = "./vimium-master"

class AutoChromeAgent(autogen.AssistantAgent):

    def __init__(
        self,
        **kwargs,
    ):

        super().__init__(
            **kwargs,
        )
        self.context = (
            sync_playwright()
            .start()
            .chromium.launch_persistent_context(
                "",
                headless=False,
                args=[
                    f"--disable-extensions-except={vimium_path}",
                    f"--load-extension={vimium_path}",
                ],
                ignore_https_errors=True,
            )
        )

        self.page = self.context.new_page()
        self.page.set_viewport_size({"width": 1080, "height": 720})

        self.driver.implicitly_wait(5)  # Wait for elements to load
        
        self.register_reply(autogen.AssistantAgent, AutoChromeAgent.perform_action)
        self.register_reply(autogen.AssistantAgent, AutoChromeAgent.navigate)
        self.register_reply(autogen.AssistantAgent, AutoChromeAgent.type)
        self.register_reply(autogen.AssistantAgent, AutoChromeAgent.click)
        self.register_reply(autogen.AssistantAgent, AutoChromeAgent.capture)


    def perform_action(self, action):
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
