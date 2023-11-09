"""Tool that calls Selenium."""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


from selenium.webdriver.common.by import By
import unidecode

import json
import re
import time
from typing import Any, Dict, List, Optional

import validators
from bs4 import BeautifulSoup


class LoggingWebDriver(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, url):
        with open("selenium_commands.log", "a") as f:
            f.write(f"Visited URL: {url}\n")
        super().get(url)

    def find_element(self, by, value):
        element = super().find_element(by, value)
        return LoggingWebElement(element._parent, element._id, by, value)

    def find_elements(self, by, value):
        elements = super().find_elements(by, value)
        return [LoggingWebElement(element._parent, element._id, by, value) for element in elements]

### Main Content Extraction ###
def is_complete_sentence(text: str) -> bool:
    return re.search(r"[.!?]\s*$", text) is not None


def get_all_text_elements(driver: LoggingWebDriver) -> List[str]:
    xpath = (
        "//*[not(self::script or self::style or"
        " self::noscript)][string-length(normalize-space(text())) > 0]"
    )
    elements = driver.find_elements(By.XPATH, xpath)
    texts = [
        element.text.strip()
        for element in elements
        if element.text.strip()
        and element.is_displayed()
        and element_completely_viewable(driver, element)
    ]
    return texts


def find_interactable_elements(driver: LoggingWebDriver) -> List[str]:
    """Find all interactable elements on the page."""
    # Extract interactable components (buttons and links)
    buttons = driver.find_elements(By.XPATH, "//button")
    links = driver.find_elements(By.XPATH, "//a")

    interactable_elements = buttons + links

    interactable_output = []
    for element in interactable_elements:
        if (
            element.is_displayed()
            and element_completely_viewable(driver, element)
            and element.is_enabled()
        ):
            element_text = element.text.strip()
            if element_text and element_text not in interactable_output:
                element_text = prettify_text(element_text, 50)
                interactable_output.append(element_text)
    return interactable_output


def prettify_text(text: str, limit: Optional[int] = None) -> str:
    """Prettify text by removing extra whitespace and converting to lowercase."""
    text = re.sub(r"\s+", " ", text)
    text = text.strip().lower()
    text = unidecode(text)
    if limit:
        text = text[:limit]
    return text


def element_completely_viewable(driver: LoggingWebDriver, elem: WebElement) -> bool:
    """Check if an element is completely viewable in the browser window."""
    elem_left_bound = elem.location.get("x")
    elem_top_bound = elem.location.get("y")
    elem_right_bound = elem_left_bound
    elem_lower_bound = elem_top_bound

    win_upper_bound = driver.execute_script("return window.pageYOffset")
    win_left_bound = driver.execute_script("return window.pageXOffset")
    win_width = driver.execute_script("return document.documentElement.clientWidth")
    win_height = driver.execute_script("return document.documentElement.clientHeight")
    win_right_bound = win_left_bound + win_width
    win_lower_bound = win_upper_bound + win_height

    return all(
        (
            win_left_bound <= elem_left_bound,
            win_right_bound >= elem_right_bound,
            win_upper_bound <= elem_top_bound,
            win_lower_bound >= elem_lower_bound,
        )
    )


def find_parent_element_text(elem: LoggingWebDriver, prettify: bool = True) -> str:
    """Find the text up to third order parent element."""
    parent_element_text = elem.text.strip()
    if parent_element_text:
        return (
            parent_element_text if not prettify else prettify_text(parent_element_text)
        )
    elements = elem.find_elements(By.XPATH, "./ancestor::*[position() <= 3]")
    for parent_element in elements:
        parent_element_text = parent_element.text.strip()
        if parent_element_text:
            return (
                parent_element_text
                if not prettify
                else prettify_text(parent_element_text)
            )
    return ""


def truncate_string_from_last_occurrence(string: str, character: str) -> str:
    """Truncate a string from the last occurrence of a character."""
    last_occurrence_index = string.rfind(character)
    if last_occurrence_index != -1:
        truncated_string = string[: last_occurrence_index + 1]
        return truncated_string
    else:
        return string

def _get_google_search_results(driver: LoggingWebDriver) -> List[Dict[str, Any]]:
    """Scrape search results from Google."""
    results = []
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    search_results = soup.find_all("div", class_="g")
    for _, result in enumerate(search_results, start=1):
        if result.find("a") and result.find("h3"):
            title_element = result.find("h3")
            link_element = result.find("a")

            title = title_element.get_text()
            link = link_element.get("href")
            if title and link:
                results.append({
                    "title": title,
                    "link": link,
                })
    return results

def _get_website_main_content(driver: LoggingWebDriver) -> str:
    """Extract the main content from a website."""
    texts = get_all_text_elements(driver)
    pretty_texts = [prettify_text(text) for text in texts]
    if not pretty_texts:
        return ""

    description = (
        "Current window displays the following contents, try scrolling up or down"
        " to view more: "
    )
    description += json.dumps(pretty_texts)

    return description

def _get_interactable_elements(driver: LoggingWebDriver) -> str:
    """Extract interactable components (buttons and links) from a website."""
    interactable_elements = driver.find_elements(
        By.XPATH,
        "//button | //div[@role='button'] | //a | //input[@type='checkbox']",
    )

    interactable_texts = []
    for element in interactable_elements:
        button_text = find_parent_element_text(element)
        button_text = prettify_text(button_text, 50)
        if (
            button_text
            and button_text not in interactable_texts
            and element.is_displayed()
            and element.is_enabled()
        ):
            interactable_texts.append(button_text)

    buttons_text = [text for text in interactable_texts if not validators.url(text)]
    links_text = [text for text in interactable_texts if validators.url(text)]
    
    interactable_output = ""
    if links_text:
        interactable_output += f"Goto these links: {json.dumps(links_text)}\n"
    if buttons_text:
        interactable_output += f"Click on these buttons: {json.dumps(buttons_text)}"

    return interactable_output

def _find_form_fields(driver: LoggingWebDriver, url: Optional[str] = None) -> str:
    """Find form fields on a website."""
    if url and url != driver.current_url and url.startswith("http"):
        try:
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(url)
            time.sleep(5)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except WebDriverException as e:
            return f"Error loading url {url}, message: {e.msg}"

    fields = []
    try:
        for element in driver.find_elements(By.XPATH, "//textarea | //input"):
            label_txt = (
                element.get_attribute("name")
                or element.get_attribute("aria-label")
                or find_parent_element_text(element)
            )
            if (
                label_txt
                and "\n" not in label_txt
                and len(label_txt) < 100
                and label_txt not in fields
            ):
                label_txt = prettify_text(label_txt)
                fields.append(label_txt)
    except StaleElementReferenceException:
        # Handle the exception and maybe retry or log the error
        pass

    return str(fields)

def clear_selenium_commands_log():
    with open("selenium_commands.log", "w") as f:
        f.write("")

def generate_selenium_code(log_file, test_file):
    key_map = {
        '\ue009a': ('Keys.CONTROL', 'a'),
        'Keys.END': 'Keys.END',
        'Keys.ENTER': 'Keys.ENTER',
    }

    with open(log_file, 'r') as log, open(test_file, 'w') as test:
        # Write the initial setup for the Selenium test
        test.write("from selenium import webdriver\n")
        test.write("from selenium.webdriver.common.by import By\n")
        test.write("from selenium.webdriver.common.keys import Keys\n\n")
        test.write("from selenium.webdriver.common.action_chains import ActionChains\n\n")
        test.write("driver = webdriver.Chrome()\n\n")
        test.write("driver.implicitly_wait(10)\n\n")

        for line in log:
            if "Visited URL:" in line:
                url = line.split("Visited URL:")[1].strip()
                test.write(f"driver.get('{url}')\n")
            elif "Clicking on element located by" in line or "Sending keys" in line:
                components = line.split("by")[1].split("=")
                by = components[0].strip()
                value = "=".join(components[1:]).strip().strip("'")
                if "Clicking on element located by" in line:
                    test.write(f"driver.find_element(By.{by.upper()}, \"{value}\").click()\n")
                elif "Sending keys" in line:
                    keys = line.split("keys")[1].split("to")[0].strip(" []").strip("'")
                    # Check if the key is in our map
                    if keys in key_map:
                        mapped_value = key_map[keys]
                        if isinstance(mapped_value, tuple):
                            keys_sequence = ", ".join(mapped_value)
                            test.write(f"driver.find_element(By.{by.upper()}, \"{value}\").send_keys({keys_sequence})\n")
                        else:
                            test.write(f"driver.find_element(By.{by.upper()}, \"{value}\").send_keys({mapped_value})\n")
                    else:
                        test.write(f"driver.find_element(By.{by.upper()}, \"{value}\").send_keys(\"{keys}\")\n")

            elif "ActionChains Clicked on element:" in line:
                text = re.search(r"text: (.+?)(,|$)", line).group(1).strip()
                tag_name = re.search(r"tag_name: (\w+),", line).group(1).strip()
                test.write(f"element = driver.find_element(By.XPATH, \"//{tag_name}[text()='{text}']\")\n")
                test.write("element.click()\n")

        # Close the driver at the end of the test
        test.write("\ndriver.quit()\n")

def wipe_selenium_code():
    with open("selenium_code.py", "w") as f:
        f.write("")
    

class LoggingActionChains(ActionChains):
    def __init__(self, driver):
        super().__init__(driver)
        self._last_moved_element = None

    def move_to_element(self, to_element):
        self._last_moved_element = to_element
        return super().move_to_element(to_element)

    def click(self, on_element=None):
        with open("selenium_commands.log", "a") as f:
            target_element = on_element or self._last_moved_element
            if target_element and isinstance(target_element, WebElement):
                element_info = self._describe_element(target_element)
                f.write(f"ActionChains Clicked on element: {element_info}\n")
            else:
                f.write("ActionChains Clicked\n")
        return super().click(on_element=on_element)

    def _describe_element(self, element):
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

class LoggingWebElement(WebElement):
    def __init__(self, parent, id_, by=None, value=None):
        super().__init__(parent, id_)
        self._by = by
        self._value = value

    def click(self):
        self._log(f"Clicking on element located by {self._by}='{self._value}'")
        super().click()

    def send_keys(self, *value):
        readable_keys = self._translate_keys(value)
        self._log(f"Sending keys {readable_keys} to element located by {self._by}='{self._value}'")
        super().send_keys(*value)

    def find_element(self, by, value):
        element = super().find_element(by, value)
        return LoggingWebElement(element._parent, element._id, by, value)

    def find_elements(self, by, value):
        elements = super().find_elements(by, value)
        return [LoggingWebElement(element._parent, element._id, by, value) for element in elements]

    def _log(self, message):
        with open("selenium_commands.log", "a") as f:
            f.write(message + "\n")

    def _translate_keys(self, keys):
        special_keys = {
            '\ue009': 'Keys.CONTROL',
            '\ue017': 'Keys.END',
            '\ue006': 'Keys.ENTER',
            # Add other special keys as needed
        }
        return [special_keys.get(key, key) for key in keys]
