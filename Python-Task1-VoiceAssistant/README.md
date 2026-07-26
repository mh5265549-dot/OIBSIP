# Oasis Infobyte Python Development Internship

## Task 1: Advanced Voice Assistant

A Python-based virtual assistant that captures voice commands via a microphone, processes user intent, provides real-time text-to-speech audio feedback, and integrates with external web services and APIs.

---

### Features & Functionality
- **Voice Recognition:** Captures spoken input using the `speech_recognition` library with dynamic energy threshold adjustments and microphone indexing.
- **Text-to-Speech Output:** Translates assistant text responses into clear audio feedback using `pyttsx3`.
- **System Utilities:** Tells current system time and date on command.
- **Web Integrations:** Automatically performs Google searches and opens browser tabs for specific queries or platforms like YouTube.
- **Live Weather API:** Fetches real-time weather details for any user-specified city using the OpenWeatherMap API.
- **Robust Error Handling:** Manages timeouts, unrecognized speech, and hardware audio errors gracefully without crashing the execution loop.

---

### Tech Stack
- **Language:** Python 3.x
- **Libraries:** 
  - `SpeechRecognition` (Microphone audio capture & Google Web Speech API wrapper)
  - `pyttsx3` (Offline text-to-speech engine)
  - `requests` (HTTP requests for live weather data fetching)
  - `webbrowser` & `datetime` (Built-in standard libraries)

---

### Setup and Installation Instructions

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/OIBSIP.git](https://github.com/YOUR-USERNAME/OIBSIP.git)
