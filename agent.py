import autogen

from autogen import AssistantAgent

from typing import Any, Dict, List, Optional

import time

import time
from io import BytesIO

from PIL import Image
from playwright.sync_api import sync_playwright
from vimbot import Vimbot
from vision import get_actions

vimium_path = "./vimium-master"

class BrowsingAgent(AssistantAgent):

    def __init__(
        self,
        **kwargs,
    ):

        super().__init__(
            **kwargs,
        )
        self.objective = "go to zeit.de and click the first article"

        self.driver = Vimbot()

        print("Navigating to Google...")
        self.driver.navigate("https://www.google.com")
        
        self.register_function({
            "next_action": self.next_action,
        })


    def next_action(self):
        time.sleep(1)
        print("Capturing the screen...")
        screenshot = self.driver.capture()
        print("Getting actions for the given objective...")
        action = get_actions(screenshot, self.objective)
        print(f"JSON Response: {action}")
        if self.driver.perform_action(action):  # returns True if done
            return True, None
        return False, None
        
