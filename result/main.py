llm_config = {
    "functions": [
        # ... existing functions ...

        # Function to initialize the webdriver
        {
            "name": "initialize_webdriver",
            "description": "Initializes a web browser for automation.",
            "parameters": {}
        },

        # Function to perform a Google search
        {
            "name": "google_search",
            "description": "Performs a Google search for a given query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to submit to Google."
                    }
                },
                "required": ["query"]
            }
        },

        # Function to move back to the previous webpage
        {
            "name": "previous_webpage",
            "description": "Navigates back to the previous webpage.",
            "parameters": {}
        },

        # Function to provide a description of the current website
        {
            "name": "describe_website",
            "description": "Provides a description of the current webpage.",
            "parameters": {}
        },

        # Function to close the webdriver
        {
            "name": "close_webdriver",
            "description": "Closes the web browser and cleans up resources.",
            "parameters": {}
        },

        # Function to click a button by matching text
        {
            "name": "click_button_by_text",
            "description": "Clicks a button on the webpage by matching text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text of the button to click."
                    }
                },
                "required": ["text"]
            }
        },

        # Function to find form inputs on the webpage
        {
            "name": "find_form_inputs",
            "description": "Finds input fields in a form on the webpage.",
            "parameters": {}
        },

        # Function to scroll the webpage
        {
            "name": "scroll",
            "description": "Scrolls the webpage in a specified direction and amount.",
            "parameters": {
                "type": "object",
                "properties": {
                    "direction": {
                        "type": "string",
                        "description": "Direction to scroll ('up' or 'down')."
                    },
                    "amount": {
                        "type": "integer",
                        "description": "Amount to scroll."
                    }
                },
                "required": ["direction", "amount"]
            }
        }
    ]
}