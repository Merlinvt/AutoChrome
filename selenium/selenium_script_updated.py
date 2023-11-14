
# Standard imports and helper logging functions will be placed at the beginning of the file
import os
import re
import json
import time
import urllib.parse
from typing import Any, Dict, List, Optional

import validators
from selenium import webdriver
from selenium.webdriver import ActionChains, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Helper functions definitions
def log_action(message):
    with open("selenium_commands.log", "a") as f:
        f.write(message + "\n")

def describe_element(element):
    attributes_to_log = ['id', 'name', 'class', 'tag_name', 'text']
    description = []

    for attr in attributes_to_log:
        try:
            value = getattr(element, attr)
            if value:
                description.append(f"{attr}: {value}")
        except Exception:
            pass

    return ', '.join(description)

def translate_keys(keys):
    special_keys = {
        Keys.CONTROL: 'Keys.CONTROL',
        Keys.END: 'Keys.END',
        Keys.ENTER: 'Keys.ENTER',
        # Add other special keys as needed
    }
    return [special_keys.get(key, key) for key in keys]

# ... all other imports if necessary ...

# ... Define initialize_webdriver and close_webdriver as already discussed ...

# Define your initialize_webdriver and close_webdriver functions here

# Continue with modified code from the user's code snippet, replacing LoggingWebDriver,
# LoggingActionChains, and LoggingWebElement with the regular webdriver, ActitonChains, and WebElement.
