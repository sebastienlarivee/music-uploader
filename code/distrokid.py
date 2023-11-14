from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os


class DistroKidNavigator:
    def __init__(self, webdriver_path, email, password):
        self.webdriver_path = webdriver_path
        self.driver = None
        self.email = email
        self.password = password
        self.main_folder = "resources/albums"

    def start_browser(self):
        # Setup Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(
            "detach", True
        )  # Stops chrome from closing when the code finishes

        # Initialize the Chrome driver with the specified path
        self.driver = webdriver.Chrome(
            service=Service(self.webdriver_path), options=chrome_options
        )

    def login(self):
        sign_in_button = self.driver.find_element(By.ID, "signInButtonFrontPage")
        sign_in_button.click()

        sign_in_email = self.driver.find_element(By.ID, "inputSigninEmail")
        sign_in_password = self.driver.find_element(By.ID, "inputSigninPassword")
        sign_in_button_2 = self.driver.find_element(By.ID, "signinButton")

        sign_in_email.send_keys(self.email)
        time.sleep(1)

        sign_in_password.send_keys(self.password)
        time.sleep(1)

        sign_in_button_2.click()

        input("Press Enter to continue...")

    def upload_album(self, album):
        how_many_songs = self.driver.find_element(By.ID, "howManySongsOnThisAlbum")
        how_many_songs.click()
        select_how_many_songs = self.driver.find_element(By.LINK_TEXT, "12 songs")
        select_how_many_songs.click()

    def distrokid_upload_auto(self):
        if self.driver is None:
            self.start_browser()

        self.driver.get("https://distrokid.com/")

        self.login()

        upload_music = self.driver.find_element(
            By.XPATH, '//button[text()="Upload music"]'
        )  # let's see if this works
        upload_music.click()

        check_snap = self.driver.find_element(By.ID, "chksnap")
        check_snap.click()

        for albums in os.listdir(self.main_folder):
            album = os.path.join(self.main_folder, albums)
            if not os.path.isfile(album):
                self.upload_album(album=album)


# Usage:
# navigator = DistroKidNavigator(webdriver_path='path/to/webdriver')
# navigator.navigate_to_distrokid()
