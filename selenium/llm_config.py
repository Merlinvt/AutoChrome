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
        
                # Function to perform a Google search
        {
            "name": "fill_out_form",
            "description": "Fills out a form on a webpage. The function takes an optional form input as a JSON string and additional keyword arguments. If the form input is a valid JSON string, it is used; otherwise, the keyword arguments are used as form inputs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The main input for the form as a JSON string, optional. If provided, should be a valid JSON string representing form fields and values."
                    },
                    "kwargs": {
                        "type": "object",
                        "description": "Additional keyword arguments representing form fields and their values, used if 'form_input' is not provided or invalid."
                    }
                },
                "required": ["query"]
            }
        },

        {
            "name": "previous_webpage",
            "description": "Navigates back to the previous webpage and returns a description.",
            "parameters": {
                "type": "object",
                "properties": {
                },
                "required": []  # No required parameters, it is optional
            }
        },

        # Function to provide a description of the current website with optional detail level
        {
            "name": "describe_website",
            "description": "Provides a description of the current webpage with optional detail level.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "url"
                    },
                },
                "required": []  # No required parameters, it is optional
            }
        },


        # Function configuration for close_webdriver
        {
            "name": "close_webdriver",
            "description": "Closes the web browser and cleans up resources.",
            "parameters": {
                "type": "object",
                "properties": {
                },
                "required": []  # No required parameters, it is optional
            }
            
        },


        # Function to click a button by matching text
        {
            "name": "click_button_by_text",
            "description": "Clicks a button on the webpage by matching text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "button_text": "string",
                        "description": "Text of the button to click."
                    }
                },
                "required": ["button_text"]
            }
        },

        # Function to find form inputs on the webpage with an optional form identifier
        {
            "name": "find_form_inputs",
            "description": "Finds input fields in a specified form on the webpage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "url"
                    },
                },
                "required": []  # Not required if default behavior is to find the first or all forms
            }
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

                },
                "required": ["direction"]
            }
        },
        
        {
            "name": "get_url",
            "description": "Navigates to a specified URL and logs the action.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to navigate to."
                    }
                },
                "required": ["url"]
            }
        }

    ]

