import datetime
import os
import webbrowser
import requests
import speech_recognition as sr
import pyttsx3

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 175)  # Speeding up or slowing down speech
engine.setProperty('volume', 1.0) # Volume level from 0.0 to 1.0

def print_banner():
    """Prints internship title card info for video recording (first 2 seconds)."""
    print("=" * 65)
    print("  INTERNSHIP SUBMISSION: OASIS INFOBYTE")
    print("  Name: Hashir Shoaib")
    print("  Track: Python Programming")
    print("  Task Title: Task 1 - Advanced Voice Assistant")
    print("=" * 65 + "\n")

def speak(text):
    """Converts text string into spoken audio feedback."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def get_mic_device_index():
    """Finds the best hardware microphone index (e.g., Realtek Microphone Array)."""
    try:
        mic_names = sr.Microphone.list_microphone_names()
        for idx, name in enumerate(mic_names):
            if "microphone array" in name.lower():
                return idx
    except Exception:
        pass
    return None

def listen_command():
    """Captures voice input from the microphone with optimized sensitivity settings."""
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.energy_threshold = 300  # Sensitivity base
    r.pause_threshold = 0.8

    mic_idx = get_mic_device_index()
    mic_args = {"device_index": mic_idx} if mic_idx is not None else {}

    try:
        with sr.Microphone(**mic_args) as source:
            print("\n[Microphone Active] Speak clearly into your mic...")
            r.adjust_for_ambient_noise(source, duration=0.6)
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            print("Recognizing speech...")
            query = r.recognize_google(audio, language='en-US')
            print(f"User said: {query}")
            return query.lower()
    except sr.WaitTimeoutError:
        print("[No speech detected. Tip: You can also type commands if your mic is muted.]")
        return ""
    except sr.UnknownValueError:
        print("[Speech Recognition could not decipher the audio]")
        speak("I couldn't understand that clearly. Please try speaking a bit louder.")
        return ""
    except sr.RequestError:
        speak("Network error. Please check your internet connection for speech processing.")
        return ""
    except Exception as e:
        print(f"[Microphone Error]: {e}")
        speak("Microphone audio error. Please check your microphone connection.")
        return ""

def get_weather(city="London"):
    """Fetches live weather updates using the OpenWeatherMap API."""
    # Replace with your free OpenWeatherMap API key
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] != "404":
            main_data = data["main"]
            weather_desc = data["weather"][0]["description"]
            temp = main_data["temp"]
            return f"The current temperature in {city} is {temp} degrees Celsius with {weather_desc}."
        else:
            return "City not found. Please check the city name."
    except Exception as e:
        print(f"Weather API Error: {e}")
        return "Unable to fetch live weather updates at the moment."

def run_assistant():
    """Main execution loop for the voice assistant."""
    print_banner()
    speak("Hello! I am your advanced virtual assistant. How can I help you today?")
    
    while True:
        command = listen_command()
        
        if not command:
            continue

        # Speak back the recognized question/command so the user hears what was understood
        speak(f"You asked: {command}")

        # 1. Greeting Response
        if "hello" in command or "hi" in command:
            speak("Hello there! How can I assist you today?")

        # 2. Time and Date Request
        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}.")

        elif "date" in command:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today's date is {current_date}.")

        # 3. Web Search / Browser Integration
        elif "search" in command or "open google for" in command:
            search_query = command.replace("search", "").replace("open google for", "").strip()
            if search_query:
                speak(f"Searching the web for {search_query}")
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
            else:
                speak("What would you like me to search for?")
                follow_up = listen_command()
                if follow_up:
                    speak(f"Searching the web for {follow_up}")
                    webbrowser.open(f"https://www.google.com/search?q={follow_up}")

        elif "open youtube" in command:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        # 4. Weather Update Integration
        elif "weather" in command:
            speak("Which city's weather would you like to check?")
            city_query = listen_command()
            if city_query:
                speak(f"Checking weather for {city_query}")
                weather_info = get_weather(city_query)
                speak(weather_info)
            else:
                speak("Defaulting to London weather.")
                speak(get_weather("London"))

        # 5. Exit Trigger
        elif "exit" in command or "stop" in command or "goodbye" in command:
            speak("Goodbye! Have a wonderful day ahead.")
            break

        else:
            speak("I am not programmed to handle that command yet, but you can try asking for the time, date, weather, or a web search.")

if __name__ == "__main__":
    run_assistant()
