selenium_functions = [
        {
            "name": "python",
            "description": "run cell in ipython and return the execution result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cell": {
                        "type": "string",
                        "description": "Valid Python cell to execute.",
                    }
                },
                "required": ["cell"],
            },
        },
        {
            "name": "sh",
            "description": "run a shell script and return the execution result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": "Valid shell script to execute.",
                    }
                },
                "required": ["script"],
            },
        },
        # ... existing functions ...

        # Function to initialize the webdriver
        
        {
            "name": "initialize_webdriver",
            "description": "Initializes a web browser for automation with optional parameters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "headless": {
                        "type": "boolean",
                        "description": "Whether to start the browser in headless mode."
                    },
                },
                "required": []  # No required parameters, they are all optional
            }
        },

        # Function to perform a Google search
        {
            "name": "google_search",
            "description": "Performs a Google search for a given query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "driver": {
                        #"type": "LoggingWebDriver",
                        "description": "Webdriver instance initialised with initialize_webdriver()"
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query to submit to Google."
                    }
                },
                "required": ["driver","query"]
            }
        },

        # Function configuration for previous_webpage
        {
            "name": "previous_webpage",
            "description": "Navigates back to the previous webpage and returns a description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "driver": {
                        #"type": "LoggingWebDriver",
                        "description": "Webdriver instance initialised with initialize_webdriver()"
                    },
                },
                "required": ["driver"]  # The driver object is required to navigate back
            }
        },

        # Function to provide a description of the current website with optional detail level
        {
            "name": "describe_website",
            "description": "Provides a description of the current webpage with optional detail level.",
            "parameters": {
                "type": "object",
                "properties": {
                    "driver": {
                        #"type": "LoggingWebDriver",
                        "description": "Webdriver instance initialised with initialize_webdriver()"
                    },
                    "url": {
                        "type": "string",
                        "description": "url"
                    },
                },
                "required": ["driver"]  # No required parameters, it is optional
            }
        },


        # Function configuration for close_webdriver
        {
            "name": "close_webdriver",
            "description": "Closes the web browser and cleans up resources.",
            "parameters": {
                "type": "object",
                "properties": {
                    "driver": {
                        #"type": "LoggingWebDriver",
                        "description": "Webdriver instance initialised with initialize_webdriver()"
                    },
                },
                "required": ["driver"]  # The driver object is required to close the WebDriver
            }
        },


        # Function to click a button by matching text
        {
            "name": "click_button_by_text",
            "description": "Clicks a button on the webpage by matching text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "driver": {
                        #"type": "LoggingWebDriver",
                        "description": "Webdriver instance initialised with initialize_webdriver()"
                    },
                    "text": {
                        "type": "string",
                        "description": "Text of the button to click."
                    }
                },
                "required": ["driver","button_text"]
            }
        },

        # Function to find form inputs on the webpage with an optional form identifier
        {
            "name": "find_form_inputs",
            "description": "Finds input fields in a specified form on the webpage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "driver": {
                        #"type": "LoggingWebDriver",
                        "description": "Webdriver instance initialised with initialize_webdriver()"
                    },
                    "url": {
                        "type": "string",
                        "description": "url"
                    },
                },
                "required": ["driver"]  # Not required if default behavior is to find the first or all forms
            }
        },

        # Function to scroll the webpage
        {
            "name": "scroll",
            "description": "Scrolls the webpage in a specified direction and amount.",
            "parameters": {
                "type": "object",
                "properties": {
                    "driver": {
                        #"type": "LoggingWebDriver",
                        "description": "Webdriver instance initialised with initialize_webdriver()"
                    },
                    "direction": {
                        "type": "string",
                        "description": "Direction to scroll ('up' or 'down')."
                    },

                },
                "required": ["driver", "direction"]
            }
        },
        
        {
            "name": "get_url",
            "description": "Navigates the WebDriver to a specified URL and logs the action.",
            "parameters": {
                "type": "object",
                "properties": {
                    "driver": {
                        "type": "object",
                        "description": "An instance of Chrome WebDriver."
                    },
                    "url": {
                        "type": "string",
                        "description": "The URL to navigate to."
                    }
                },
                "required": ["driver", "url"]
            }
        }

    ]

