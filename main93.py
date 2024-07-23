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
import cv2  # Import OpenCV for the camera function

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to speak a text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to introduce the assistant
def about_me():
    speak("I am Mindless, your voice assistant created by Prakriti . I can help you with various tasks like fetching weather, playing YouTube videos, and more.")


# Function to fetch news
def fetch_news():
    news_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_NEWSAPI_KEY"
    response = requests.get(news_url).json()
    news_list = [article['title'] for article in response['articles']]
    return news_list


# Function to fetch a random fact
def fetch_random_facts():
    facts = [
        "The Eiffel Tower can be 15 cm taller during the summer.",
        "Honey never spoils.",
        "A group of flamingos is called a 'flamboyance'."
    ]
    fact = random.choice(facts)
    speak(fact)
    print(fact)

# Function to tell a joke
def tell_joke():
    jokes = [
        "Why do chicken coops only have two doors? Because if they had four, they would be chicken sedans.",
        "What do you call fake spaghetti? An impasta!",
        "Why don't scientists trust atoms? Because they make up everything!"
    ]
    joke = random.choice(jokes)
    speak(joke)
    print(joke)

# Function to fetch weather
def fetch_weather():
    city = "New York"  # Default city
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your OpenWeatherMap API key
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(weather_url).json()

    if response.get("cod") != 200:
        speak(f"Sorry, I couldn't fetch the weather for {city}.")
        print(f"Error fetching weather: {response.get('message', 'Unknown error')}")
        return

    try:
        weather = response['weather'][0]['description']
        temp = response['main']['temp']
        speak(f"The current weather in {city} is {weather} with a temperature of {temp} degrees Celsius.")
        print(f"The current weather in {city} is {weather} with a temperature of {temp} degrees Celsius.")
    except KeyError as e:
        speak(f"Sorry, I couldn't retrieve the weather information. Please try again later.")
        print(f"Error: Missing key in API response - {e}")
    except Exception as e:
        speak(f"Sorry, there was an error fetching the weather information.")
        print(f"An error occurred: {e}")

# Function to open a specified website
def open_website(url, search_text=None):
    try:
        # Setup WebDriver
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')  # Open the browser in maximized mode
        driver = webdriver.Chrome(service=service, options=options)
        
        # Open the specified website
        if search_text:
            driver.get(f"{url}/search?q={search_text}")
            speak(f"Searching for {search_text} on {url}.")
            print(f"Searching for {search_text} on {url}.")
        else:
            driver.get(url)
            speak(f"I have opened {url}.")
            print(f"I have opened {url}.")
        
        # Wait for user input to close the browser
        input("Press Enter to close the browser...")
        driver.quit()
    except Exception as e:
        speak(f"Sorry, I encountered an error while trying to open the website.")
        print(f"Error: {e}")

# Function to perform a Google search
def google_search(query):
    open_website("https://www.google.com", search_text=query)

# Function to perform a Google Maps search
def google_maps_search(location):
    open_website("https://www.google.com/maps", search_text=location)

# Function to open Poki
def open_poki():
    open_website("https://www.poki.com")

# Function to open Amazon
def open_amazon():
    open_website("https://www.amazon.com")

# Function to open YouTube
def open_youtube():
    open_website("https://www.youtube.com")

# Function to open Facebook
def open_facebook():
    open_website("https://www.facebook.com")

# Function to open the camera
def open_camera():
    speak("Opening the camera.")
    print("Opening the camera.")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# Function to listen for a topic
def listen_for_topic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        speak("What topic do you need information about?")
        print("Listening for topic...")
        audio = r.listen(source, timeout=10)
        topic = r.recognize_google(audio)
        print(f"Topic: {topic}")
        return topic.lower()

# Function to listen for a video
def listen_for_video():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        speak("What video would you like to play?")
        print("Listening for video...")
        audio = r.listen(source, timeout=10)
        video = r.recognize_google(audio)
        print(f"Video: {video}")
        return video

# Function to play a video on YouTube
def play_youtube_video(video):
    url = f"https://www.youtube.com/results?search_query={video}"
    open_website(url)

# Main function to handle voice commands
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
                continue  # Continue to the next iteration to listen again
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                speak("Sorry, there was an error with the speech recognition service. Please try again later.")
                continue  # Continue to the next iteration to listen again
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase to start")
                speak("I didn't hear anything. Can you please say that again?")
                continue  # Continue to the next iteration to listen again

        # Convert text to lower case for case-insensitive matching
        text = text.lower()

        # Respond based on the user's input
        if "tell me about yourself" in text or "about yourself" in text:
            about_me()  # Call the function to introduce the assistant

        elif "what" in text and "about" in text and "you" in text:
            speak("I am having a good day.")

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

        elif "open" in text.lower():
            if "amazon" in text.lower():
                open_website("https://www.amazon.com", "Amazon")
        elif "youtube" in text.lower():
                open_website("https://www.youtube.com", "YouTube")
        elif "wikipedia" in text.lower():
                open_website("https://www.wikipedia.org", "Wikipedia")
        elif "pinterest" in text.lower():
                open_website("https://www.pinterest.com", "Pinterest")
        elif "myntra" in text.lower():
                open_website("https://www.myntra.com", "Myntra")
        elif "flipkart" in text.lower():
                open_website("https://www.flipkart.com", "Flipkart")
            
        elif "quit" in text or "exit" in text or "bye" in text:
            speak("Goodbye! Have a nice day.")
            break

        else:
            speak("Sorry, I didn't understand that. Can you please repeat?")


if __name__ == "__main__":
    main()  