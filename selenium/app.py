from functions import (
    initialize_webdriver,
    google_search,
    get_url,
    describe_website,
)

#initialize_webdriver()
get_url("https://www.zeit.de/index")
print(describe_website())
#get_url("https://www.zeit.de/index")
#google_search("hi")
