from functions import (
    initialize_webdriver,
    google_search
)

driver = initialize_webdriver(False)
reult = google_search(driver,"hi")
print(reult)