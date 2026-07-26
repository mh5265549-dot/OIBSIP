# Oasis Infobyte Python Development Internship

## Task 4: Advanced Weather App

A Python-based graphical user interface (GUI) weather application that pulls real-time weather metrics, multi-day forecasts, remote icons, and automatic IP location resolution.

### Features & Functionality
- **Interactive GUI:** Built cleanly via `tkinter` with modular panels and tabbed forecast views.
- **Live Weather API Integration:** Connects securely with OpenWeatherMap REST endpoints to fetch accurate real-time metrics (temperature, humidity, wind speed, conditions).
- **Dynamic Weather Icons:** Downloads and embeds official visual weather representations utilizing `PIL` (Pillow).
- **Forecast Overviews:** Includes structured hourly breakdown tabs and 5-day outlook schedules.
- **Unit Toggle Support:** Instant conversion button switching metrics between Celsius (°C) and Fahrenheit (°F).
- **Automatic IP Geolocation:** Automatically detects local positioning using the `ipinfo.io` API.
- **GUI-Based Error Handling:** Manages invalid city names, network dropouts, and empty submissions through popup dialogues.

---

### Tech Stack
- **Language:** Python 3.x
- **Libraries:** 
  - `tkinter` (GUI architecture)
  - `requests` (HTTP requests for weather and IP lookup endpoints)
  - `PIL` (Pillow image processing for remote icon rendering)

---

### Setup and Installation Instructions

1. **Navigate to the task directory:**
   ```bash
   cd infobyte-python task4
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python weather_app.py
   ```
