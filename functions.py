functions_cfg = [ 

        {
            "name": "perform_action",
            "description": "",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "action",
                    }
                },
                "required": ["action"],
            },
        },
        
        {
            "name": "get_actions",
            "description": "",
            "parameters": {
                "type": "object",
                "properties": {
                    "screenshot": {
                        "type": "string",
                        "description": "Valid shell script to execute.",
                    },
                    "objective": {
                        "type": "string",
                        "description": "Valid shell script to execute.",
                    }
                },
                "required": ["screenshot","objective"],
            },
        },

    ]

