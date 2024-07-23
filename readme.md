#Voice Assistant: Mindless
Introduction
Mindless is a voice assistant designed to perform various tasks such as fetching weather updates, playing YouTube videos, providing news, telling jokes, and more. The assistant uses speech recognition, web scraping, and API integration to deliver information and services.

Features
1.Weather Updates: Provides current weather information.
2.News Fetching: Retrieves top news headlines.
3.Random Facts: Tells random interesting facts.
4.Jokes: Shares random jokes.
5.Wikipedia Information: Fetches information on any given topic from Wikipedia.
6.Video Playback: Plays requested videos on YouTube.
7.Website Navigation: Opens specified websites such as Google, Maps, Amazon, YouTube, and Facebook.
8.Camera Access: Opens the system's camera.
9.General Interaction: Introduces itself and interacts with the user.
Dependencies


Ensure you have the following Python packages installed:

speech_recognition
requests
pyttsx3
webbrowser
selenium
webdriver_manager
opencv-python
You can install these dependencies using pip:


bash

pip install speech_recognition requests pyttsx3 selenium webdriver_manager opencv-python


Setup and Usage
Initialize the Text-to-Speech Engine: The pyttsx3 engine is initialized to convert text to speech.
WebDriver Setup: Selenium WebDriver is used to automate web browsing. Ensure you have ChromeDriver installed and available in your PATH.
Code Explanation
Initialization
python

import speech_recognition as sr
import requests
import random
import pyttsx3
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import cv2

engine = pyttsx3.init()
Main Class: Inflow
Handles Wikipedia information fetching using Selenium.

functions 
class Inflow:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def get_info(self, topic):
        self.driver.get(f"https://en.wikipedia.org/wiki/{topic}")
        try:
            summary = self.driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/p[1]').text
            speak(summary)
            print(summary)
        except Exception as e:
            speak("Sorry, I could not find any information on that topic.")
            print("Error: No information found.")

    def quit(self):
        self.driver.quit()
Utility Functions
speak(text): Converts text to speech.
about_me(): Introduces the assistant.
fetch_news(): Fetches top news headlines using NewsAPI.
fetch_random_facts(): Tells a random fact.
tell_joke(): Tells a random joke.
fetch_weather(): Fetches current weather information using OpenWeatherMap API.
open_website(url, search_text=None): Opens a specified website, optionally performs a search.
google_search(query): Performs a Google search.
google_maps_search(location): Performs a Google Maps search.
open_poki(), open_amazon(), open_youtube(), open_facebook(): Opens specified websites.
open_camera(): Opens the system's camera.
listen_for_topic(), listen_for_video(): Listens for specific inputs from the user.
play_youtube_video(video): Plays a video on YouTube.
Main Function
Handles the voice interaction and commands.

main function 
def main():
    speak("Hello buddy, I am your voice assistant Mindless. What is up with you?")

    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            try:
                audio = r.listen(source, timeout=10)
                text = r.recognize_google(audio)
                print(text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                speak("Sorry, I didn't catch that. Can you please repeat?")
                continue
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                speak("Sorry, there was an error with the speech recognition service. Please try again later.")
                continue
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase to start")
                speak("I didn't hear anything. Can you please say that again?")
                continue

        text = text.lower()

        if "tell me about yourself" in text or "about yourself" in text:
            about_me()

        elif "what" in text and "about" in text and "you" in text:
            speak("I am having a good day ma'am")

        elif "information" in text:
            speak("You need information related to which topic?")
            topic = listen_for_topic()

            if topic:
                speak(f"Searching Wikipedia for {topic}")
                inflow_instance = Inflow()
                inflow_instance.get_info(topic)
                inflow_instance.quit()
            else:
                speak("Sorry, I didn't get that. Please try again.")

        elif "play" in text and "video" in text:
            speak("What video would you like to play on YouTube?")
            video = listen_for_video()

            if video:
                speak(f"Playing {video} on YouTube")
                play_youtube_video(video)
            else:
                speak("Sorry, I didn't catch that. Can you please repeat?")

        elif "news" in text:
            speak("Fetching the latest news headlines.")
            news = fetch_news()
            for item in news:
                speak(item)
                print(item)

        elif "random fact" in text:
            fetch_random_facts()

        elif "joke" in text:
            tell_joke()

        elif "weather" in text:
            fetch_weather()

        elif "google" in text:
            search_query = text.replace("google", "").strip()
            if search_query:
                google_search(search_query)
            else:
                speak("What would you like to search for on Google?")

        elif "maps" in text:
            location = text.replace("maps", "").strip()
            if location:
                google_maps_search(location)
            else:
                speak("Which location would you like to search for on Google Maps?")

        elif "poki" in text:
            open_poki()

        elif "amazon" in text:
            open_amazon()

        elif "youtube" in text:
            open_youtube()

        elif "facebook" in text:
            open_facebook()

        elif "camera" in text:
            open_camera()

        elif "quit" in text or "exit" in text or "bye" in text:
            speak("Goodbye! Have a nice day.")
            break

        else:
            speak("Sorry, I didn't understand that. Can you please repeat?")
    
if __name__ == "__main__":
    main()
How to Run
Ensure you have all the dependencies installed.
Run the script:


python main.py1.
Follow the voice prompts and interact with the assistant by speaking your commands.
API Keys
Replace NEWS_API_KEY and WEATHER_API_KEY with your actual API keys for NewsAPI and OpenWeatherMap respectively.