from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class DistroKidNavigator:
    def __init__(self, webdriver_path):
        self.webdriver_path = webdriver_path
        self.driver = None

    def start_browser(self):
        # Setup Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True) # Stops chrome from closing when the code finishes
        
        # Initialize the Chrome driver with the specified path
        self.driver = webdriver.Chrome(service=Service(self.webdriver_path), options=chrome_options)

    def navigate_to_distrokid(self):
        if self.driver is None:
            self.start_browser()
        
        self.driver.get("https://distrokid.com/")


# Usage:
# navigator = DistroKidNavigator(webdriver_path='path/to/webdriver') 
# navigator.navigate_to_distrokid()
