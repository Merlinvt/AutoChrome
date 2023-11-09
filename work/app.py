from main import initialize_webdriver, google_search, describe_website, close_webdriver

def main():
    try:
        # Initialize WebDriver
        driver = initialize_webdriver(headless=False)

        # Perform a Google search
        search_query = "OpenAI"
        search_results = google_search(driver, search_query)
        print("Google Search Results:")
        print(search_results)

        # Describe the first result website
        first_result_url = "https://www.openai.com"  # Replace with actual URL from search results
        website_description = describe_website(driver, first_result_url)
        print("Website Description:")
        print(website_description)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the WebDriver
        print("done")
        close_webdriver(driver)

if __name__ == "__main__":
    main()
