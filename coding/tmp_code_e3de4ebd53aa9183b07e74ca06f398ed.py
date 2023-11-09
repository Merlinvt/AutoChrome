from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setting up Chrome options
options = Options()
options.headless = False # Ensure headless is False to have a GUI
options.add_experimental_option('debuggerAddress', 'localhost:9222')

# Initializing the WebDriver with the specified options
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Navigating to google.de
driver.get("http://www.google.de")