driver = initialize_webdriver(headless=True)
search_result = google_search(driver, "example query")
print(search_result)
print(describe_website(driver))
previous_webpage(driver)
driver.quit()  # Don't forget to close the WebDriver