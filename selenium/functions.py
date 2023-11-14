"""Tool that calls Selenium."""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import StaleElementReferenceException
import json
import re
import time
import urllib.parse
from typing import Any, Dict, List, Optional

import validators


from utils import (
    find_parent_element_text,
    truncate_string_from_last_occurrence,
    _get_google_search_results,
    _get_website_main_content,
    _get_interactable_elements,
    _find_form_fields,
    clear_selenium_commands_log,
    generate_selenium_code,
    wipe_selenium_code,
    LoggingActionChains
)
from IPython import get_ipython

def exec_python(cell):
    ipython = get_ipython()
    result = ipython.run_cell(cell)
    log = str(result.result)
    if result.error_before_exec is not None:
        log += f"\n{result.error_before_exec}"
    if result.error_in_exec is not None:
        log += f"\n{result.error_in_exec}"
    return log

def exec_sh(script):
    return user_proxy.execute_code_blocks([("sh", script)])

def initialize_webdriver(headless: bool = False) -> webdriver.Chrome:
    """Initialize and return a Selenium WebDriver."""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    else:
        chrome_options.add_argument("--start-maximized")

    chrome_options.debugger_address="localhost:9222"
    #if debugger_address:
    #chrome_options.add_experimental_option("debuggerAddress", debugger_address)
    #chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")

    clear_selenium_commands_log()

    #service = Service(executable_path='/home/merlin/Documents/code/chromedriver-linux64/chromedriver')

    # Assuming the path to chromedriver is set in PATH
    #driver = webdriver.Chrome(service=service, options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(1)  # Wait for elements to load
    return driver

def fill_out_form(form_input: Optional[str] = None, **kwargs: Any) -> str:
    """fill out form by form field name and input name"""
    driver = initialize_webdriver()
    filled_element = None
    if form_input and type(form_input) == str:
        # Clean up form input
        form_input_str = truncate_string_from_last_occurrence(
            string=form_input, character="}"  # type: ignore
        )
        try:
            form_input = json.loads(form_input_str)
        except json.decoder.JSONDecodeError:
            return (
                "Invalid JSON input. Please check your input is JSON format and try"
                " again. Make sure to use double quotes for strings. Example input:"
                ' {"email": "foo@bar.com","name": "foo bar"}'
            )
    elif not form_input:
        form_input = kwargs  # type: ignore

    MAX_RETRIES = 3

    for key, value in form_input.items():
        retries = 0
        while retries < MAX_RETRIES:
            try:
                # Use explicit wait to find the element
                time.sleep(1)
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//textarea[@name='{key}'] | //input[@name='{key}']"))
                )
                # Scroll the element into view
                driver.execute_script("arguments[0].scrollIntoView();", element)

                # Clear the input field
                element.send_keys(Keys.CONTROL + "a")
                element.send_keys(Keys.DELETE)
                element.clear()

                # Send the input value
                element.send_keys(value)

                filled_element = element
                break  # Exit the while loop if successful
            except StaleElementReferenceException:
                retries += 1
                if retries == MAX_RETRIES:
                    return f"Failed to fill out form input {key} after {MAX_RETRIES} retries."
                continue
            except WebDriverException as e:
                print(e)
            return f"Error filling out form with input {form_input}, message: {e.msg}"

    if not filled_element:
        return (
            f"Cannot find form with input: {form_input.keys()}."  # type: ignore
            f" Available form inputs: {_find_form_fields()}"
        )
    before_content = describe_website()
    filled_element.send_keys(Keys.RETURN)
    after_content = describe_website()
    if before_content != after_content:
        return (
            f"Successfully filled out form with input: {form_input}, website"
            f" changed after filling out form. Now {after_content}"
        )
    else:
        return (
            f"Successfully filled out form with input: {form_input}, but"
            " website did not change after filling out form."
        )



def google_search(query: str) -> str:
    """Perform a Google search and return the results."""
    driver = initialize_webdriver()
    safe_string = urllib.parse.quote_plus(query)
    url = "https://www.google.com/search?q=" + safe_string
    try:
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)
    except Exception:
        return f"Cannot load website {url}. Try again later."

    return json.dumps(_get_google_search_results(driver))

def previous_webpage() -> str:
    """Go back in browser history."""
    driver = initialize_webdriver()
    driver.back()
    return describe_website(driver)

def describe_website(url: Optional[str] = None) -> str:
    """Describe the website."""
    driver = initialize_webdriver()
    output = ""
    if url:
        try:
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(url)
        except Exception:
            return f"Cannot load website {url}. Make sure you input the correct and complete url starting with http:// or https://."

    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1)

    try:
        main_content = _get_website_main_content(driver)
    except WebDriverException:
        return "Website still loading, please wait a few seconds and try again."
    if main_content:
        output += f"{main_content}\n"

    interactable_content = _get_interactable_elements(driver)
    if interactable_content:
        output += f"{interactable_content}\n"

    form_fields = _find_form_fields(driver)
    if form_fields:
        output += "You can input text in these fields using fill_form function: " + form_fields

    return output

def close_webdriver() -> None:
    driver = initialize_webdriver()
    """Close the Selenium WebDriver session and perform cleanup."""
    driver.close()
    wipe_selenium_code()  # Assuming this is a standalone function or a method of another class
    generate_selenium_code("selenium_commands.log", "selenium_code.py")  # Same assumption as above

def click_button_by_text(button_text: str) -> str:
    """Click a button based on its text."""
    driver = initialize_webdriver()
    if validators.url(button_text):
        return describe_website(driver, button_text)

    if driver.current_url.startswith("https://www.google.com/search"):
        google_search_results = _get_google_search_results(driver)
        for result in google_search_results:
            if button_text.lower() in result["title"].lower():
                return describe_website(driver, result["link"])

    driver.switch_to.window(driver.window_handles[-1])

    if button_text.count('"') > 1:
        try:
            button_text = re.findall(r'"([^"]*)"', button_text)[0]
        except IndexError:
            pass

    try:
        elements = driver.find_elements(
            By.XPATH,
            "//button | //div[@role='button'] | //a | //input[@type='checkbox']",
        )

        if not elements:
            return "No interactable buttons found on the website."

        selected_element = None
        all_buttons = []
        for element in elements:
            text = find_parent_element_text(element)
            if (
                element.is_displayed()
                and element.is_enabled()
                and (
                    text == button_text
                    or (
                        button_text in text
                        and abs(len(text) - len(button_text)) < 50
                    )
                )
            ):
                selected_element = element
                break
            if text:
                all_buttons.append(text)

        if not selected_element:
            return "No interactable element found with the specified text."

        actions = LoggingActionChains(driver)
        actions.move_to_element(selected_element).click().perform()

        return describe_website(driver)
    except WebDriverException as e:
        return f"Error clicking button with text '{button_text}', message: {e.msg}"

def find_form_inputs(url: Optional[str] = None) -> str:
    """Find form inputs on the website."""
    driver = initialize_webdriver()
    fields = _find_form_fields(driver, url)
    if fields:
        return "Available Form Input Fields: " + fields
    else:
        return "No form inputs found on current page."

def scroll(direction: str) -> str:
    """Scroll the webpage in the specified direction."""
    driver = initialize_webdriver()
    window_height = driver.execute_script("return window.innerHeight")
    if direction == "up":
        window_height = -window_height

    # Scroll by one window height
    driver.execute_script(f"window.scrollBy(0, {window_height})")

    return describe_website(driver)

def get_url(url: str):
    driver = initialize_webdriver()
    with open("selenium_commands.log", "a") as f:
        f.write(f"Visited URL: {url}\n")
    driver.get(url)
    
