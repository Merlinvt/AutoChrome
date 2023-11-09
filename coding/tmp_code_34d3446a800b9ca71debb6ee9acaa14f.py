from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# define the options
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
chrome_options.headless = False

# initiate the driver
driver = webdriver.Chrome(options=chrome_options)

# navigate to google.de
driver.get("https://www.google.de")