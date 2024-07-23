# assistant.py

import pyttsx3 as p
import speech_recognition as sr
from news import fetch_news
from facts import fetch_random_facts
from music import Music
from selenium_web import Inflow  # Import the Inflow class from selenium_web.py

class Assistant:
    def __init__(self):
        # Initialize the text-to-speech engine
        self.engine = p.init()
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', 180)  # Set speech rate
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Set the voice to the second one (usually female)
        print(rate)  # Print the speech rate

        # Initialize the speech recognizer
        self.r = sr.Recognizer()

    # Define the function to speak text
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    # Define a function to handle the main loop of commands
    def main(self):
        self.speak("Hello ma'am, I am your voice assistant Mindless. How are you?")

        while True:
            text = self.listen()

            if text:
                # Respond based on the user's input
                if "what" in text and "about" in text and "you" in text:
                    self.speak("I am having a good day ma'am")

                elif "information" in text:
                    self.speak("You need information related to which topic?")
                    topic = self.listen()
                    if topic:
                        self.speak(f"Searching Wikipedia for {topic}")
                        inflow_instance = Inflow()
                        inflow_instance.get_info(topic)  # Pass the recognized topic to the get_info method

                elif "play" in text and "video" in text:
                    self.speak("What song would you like to hear?")
                    song = self.listen()
                    if song:
                        self.speak(f"Playing {song} on YouTube")
                        music_instance = Music()
                        music_instance.play(song)  # Pass the recognized song to the play method

                elif "news" in text:
                    self.speak("Fetching the latest news for you.")
                    news_articles = fetch_news()
                    for article in news_articles:
                        print(article)
                        self.speak(article)

                elif "fact" in text:
                    fetch_random_facts()

                # Ask the user if they need anything else
                self.speak("Is there anything else I can help you with?")
                response = self.listen()
                if response and ("stop" in response.lower() or "that's it" in response.lower()):
                    self.speak("Alright, have a great day ma'am!")
                    break

    def listen(self):
        with sr.Microphone() as source:
            self.r.energy_threshold = 10000
            self.r.adjust_for_ambient_noise(source, duration=2.0)  # Increased duration
            print("Listening...")
            audio = self.r.listen(source)

            try:
                text = self.r.recognize_google(audio)
                print(text)
                return text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return ""
