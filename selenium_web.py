from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

class Inflow:
    def __init__(self):
        # Use ChromeDriverManager to handle the ChromeDriver setup
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def get_info(self, query):
        self.driver.get("http://www.wikipedia.org")
        
        # Find the search input element by its XPath
        search_box = self.driver.find_element("xpath", '//*[@id="searchInput"]')
        search_box.send_keys(query)
        
        # Find the search button element by its XPath and click it
        search_button = self.driver.find_element("xpath", '//*[@id="search-form"]/fieldset/button')
        search_button.click()
        
        print("Search performed. Browser is open. Press Ctrl+C to close it.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.driver.quit()
            print("Browser closed.")

class Music:
    def __init__(self):
        # Use ChromeDriverManager to handle the ChromeDriver setup
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def play(self, query):
        search_url = "https://www.youtube.com/results?search_query=" + query
        self.driver.get(search_url)
        
        # Find the first video element by its CSS selector and click it
        video = self.driver.find_element("css selector", "a#video-title")
        video.click()
        
        print("Video playing. Browser is open. Press Ctrl+C to close it.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.driver.quit()
            print("Browser closed.")

# Example usage
if __name__ == "__main__":
    inflow_instance = Inflow()
    inflow_instance.get_info("neutron")

    music_instance = Music()
    music_instance.play("lofi hip hop")
