# facts.py

import randfacts
import speech_recognition as sr

def fetch_random_facts():
    r = sr.Recognizer()
    while True:
        fact = randfacts.get_fact()
        print(f"Did you know that {fact}")

        # Simulating speech
        speak(f"Did you know that {fact}")

        print("Would you like to listen to one more fact?")
        speak("Would you like to listen to one more fact?")

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=2.0)
            audio = r.listen(source)

            try:
                response = r.recognize_google(audio)
                print(response)
                if "stop" in response.lower() or "that's it" in response.lower():
                    speak("Alright, stopping the facts.")
                    break
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

def speak(text):
    # Define this function for the facts module
    import pyttsx3 as p
    engine = p.init()
    engine.setProperty('rate', 180)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()
