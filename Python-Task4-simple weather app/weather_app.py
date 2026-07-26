import io
import tkinter as tk
from tkinter import messagebox, ttk
import requests
from PIL import Image, ImageTk

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Weather App - Oasis Infobyte")
        self.root.geometry("520x680")
        self.root.resizable(False, False)

        # State Variables
        self.unit = "C"  # "C" for Celsius or "F" for Fahrenheit
        self.temp_symbol = "°C"
        self.speed_symbol = "km/h"
        self.icon_cache = {}

        # Style Configuration
        style = ttk.Style()
        style.theme_use('clam')

        # --- TITLE BANNER ---
        banner_frame = tk.Frame(root, bg="#2c3e50", pady=8)
        banner_frame.pack(fill="x")
        tk.Label(banner_frame, text="Hashir Shoaib", font=("Arial", 11, "bold"), fg="white", bg="#2c3e50").pack()
        tk.Label(banner_frame, text="Track: Python Programming | Task 4: Advanced Weather App",
                 font=("Arial", 9), fg="#bdc3c7", bg="#2c3e50").pack()

        # --- SEARCH & CONTROLS FRAME ---
        search_frame = tk.Frame(root, pady=10, padx=15)
        search_frame.pack(fill="x")

        tk.Label(search_frame, text="City:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, sticky="w")
        self.city_entry = tk.Entry(search_frame, font=("Arial", 11), width=18)
        self.city_entry.grid(row=0, column=1, padx=5)
        self.city_entry.insert(0, "London")
        self.city_entry.bind("<Return>", lambda event: self.fetch_weather())

        tk.Button(search_frame, text="Search", font=("Arial", 9, "bold"), bg="#2980b9", fg="white",
                  padx=8, command=self.fetch_weather).grid(row=0, column=2, padx=4)

        tk.Button(search_frame, text="📍 Auto-Location", font=("Arial", 9, "bold"), bg="#27ae60", fg="white",
                  padx=8, command=self.auto_detect_location).grid(row=0, column=3, padx=4)

        self.unit_btn = tk.Button(search_frame, text="Toggle °F", font=("Arial", 9, "bold"), bg="#e67e22",
                                  fg="white", padx=6, command=self.toggle_unit)
        self.unit_btn.grid(row=0, column=4, padx=4)

        # --- CURRENT WEATHER CARD ---
        self.weather_card = tk.LabelFrame(root, text=" Current Weather ", font=("Arial", 11, "bold"), padx=15, pady=15)
        self.weather_card.pack(fill="x", padx=20, pady=5)

        self.location_label = tk.Label(self.weather_card, text="-- , --", font=("Arial", 16, "bold"), fg="#2c3e50")
        self.location_label.pack()

        self.icon_label = tk.Label(self.weather_card)
        self.icon_label.pack(pady=5)

        self.temp_label = tk.Label(self.weather_card, text="-- °C", font=("Arial", 28, "bold"), fg="#e74c3c")
        self.temp_label.pack()

        self.desc_label = tk.Label(self.weather_card, text="--", font=("Arial", 12, "italic"), fg="#7f8c8d")
        self.desc_label.pack(pady=2)

        metrics_frame = tk.Frame(self.weather_card, pady=10)
        metrics_frame.pack(fill="x")

        self.feels_label = tk.Label(metrics_frame, text="Feels Like: --", font=("Arial", 10))
        self.feels_label.grid(row=0, column=0, padx=15, pady=3, sticky="w")

        self.humidity_label = tk.Label(metrics_frame, text="Humidity: --%", font=("Arial", 10))
        self.humidity_label.grid(row=0, column=1, padx=15, pady=3, sticky="w")

        self.wind_label = tk.Label(metrics_frame, text="Wind Speed: --", font=("Arial", 10))
        self.wind_label.grid(row=1, column=0, padx=15, pady=3, sticky="w")

        self.pressure_label = tk.Label(metrics_frame, text="Pressure: -- hPa", font=("Arial", 10))
        self.pressure_label.grid(row=1, column=1, padx=15, pady=3, sticky="w")

        # --- FORECAST TABLE ---
        forecast_frame = tk.LabelFrame(root, text=" 5-Day Forecast Outlook ", font=("Arial", 11, "bold"),
                                       padx=10, pady=10)
        forecast_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("date", "max_temp", "min_temp", "desc", "humidity")
        self.forecast_tree = ttk.Treeview(forecast_frame, columns=columns, show="headings", height=5)
        self.forecast_tree.heading("date", text="Date")
        self.forecast_tree.heading("max_temp", text="Max Temp")
        self.forecast_tree.heading("min_temp", text="Min Temp")
        self.forecast_tree.heading("desc", text="Condition")
        self.forecast_tree.heading("humidity", text="Humidity")

        self.forecast_tree.column("date", width=100, anchor="center")
        self.forecast_tree.column("max_temp", width=80, anchor="center")
        self.forecast_tree.column("min_temp", width=80, anchor="center")
        self.forecast_tree.column("desc", width=150, anchor="center")
        self.forecast_tree.column("humidity", width=80, anchor="center")
        self.forecast_tree.pack(fill="both", expand=True)

        # Fetch initial weather
        self.fetch_weather()

    def toggle_unit(self):
        """Switches between Celsius and Fahrenheit."""
        if self.unit == "C":
            self.unit = "F"
            self.temp_symbol = "°F"
            self.unit_btn.config(text="Toggle °C")
        else:
            self.unit = "C"
            self.temp_symbol = "°C"
            self.unit_btn.config(text="Toggle °F")
        self.fetch_weather()

    def auto_detect_location(self):
        """Uses ipinfo.io to detect current city via IP geolocation."""
        try:
            res = requests.get("https://ipinfo.io/json", timeout=5)
            if res.status_code == 200:
                city = res.json().get("city", "")
                if city:
                    self.city_entry.delete(0, tk.END)
                    self.city_entry.insert(0, city)
                    self.fetch_weather()
                else:
                    messagebox.showwarning("Location Warning", "Could not resolve city from IP location.")
            else:
                messagebox.showwarning("Location Warning", "IP Geolocation service unavailable.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed auto-location lookup: {e}")

    def load_weather_icon(self, icon_url):
        """Downloads and caches weather condition icon from URL."""
        if icon_url in self.icon_cache:
            return self.icon_cache[icon_url]
        try:
            img_data = requests.get(f"https:{icon_url}", timeout=5).content
            image = Image.open(io.BytesIO(img_data)).resize((64, 64), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.icon_cache[icon_url] = photo
            return photo
        except Exception:
            return None

    def convert_temp(self, temp_c_str):
        """Converts temperature string from Celsius to Fahrenheit if needed."""
        try:
            temp_c = float(temp_c_str)
            if self.unit == "F":
                return f"{round(temp_c * 9/5 + 32, 1)} {self.temp_symbol}"
            return f"{temp_c} {self.temp_symbol}"
        except Exception:
            return f"-- {self.temp_symbol}"

    def fetch_weather(self):
        """Fetches current weather and 5-day forecast using the free wttr.in API (no key required)."""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Input Error", "Please enter a valid city name.")
            return

        url = f"https://wttr.in/{city}?format=j1"

        try:
            res = requests.get(url, timeout=8, headers={"User-Agent": "WeatherApp/1.0"})
            if res.status_code != 200:
                messagebox.showerror("Weather Error", f"City '{city}' not found. Please check the name.")
                return

            data = res.json()
            current = data["current_condition"][0]
            nearest_area = data["nearest_area"][0]

            city_name = nearest_area["areaName"][0]["value"]
            country = nearest_area["country"][0]["value"]
            self.location_label.config(text=f"{city_name}, {country}")

            temp_c = current["temp_C"]
            feels_c = current["FeelsLikeC"]
            humidity = current["humidity"]
            pressure = current["pressure"]
            wind_kmph = current["windspeedKmph"]
            desc = current["weatherDesc"][0]["value"]
            icon_url = current["weatherIconUrl"][0]["value"]

            self.temp_label.config(text=self.convert_temp(temp_c))
            self.desc_label.config(text=desc)
            self.feels_label.config(text=f"Feels Like: {self.convert_temp(feels_c)}")
            self.humidity_label.config(text=f"Humidity: {humidity}%")
            self.wind_label.config(text=f"Wind Speed: {wind_kmph} km/h")
            self.pressure_label.config(text=f"Pressure: {pressure} hPa")

            # Load icon
            icon_image = self.load_weather_icon(icon_url)
            if icon_image:
                self.icon_label.config(image=icon_image)
                self.icon_label.image = icon_image

            # 5-Day Forecast
            for item in self.forecast_tree.get_children():
                self.forecast_tree.delete(item)

            for day in data.get("weather", [])[:5]:
                date = day["date"]
                max_c = day["maxtempC"]
                min_c = day["mintempC"]
                day_desc = day["hourly"][4]["weatherDesc"][0]["value"] if day.get("hourly") else "--"
                avg_hum = day["hourly"][4]["humidity"] if day.get("hourly") else "--"

                max_t = self.convert_temp(max_c)
                min_t = self.convert_temp(min_c)
                self.forecast_tree.insert("", "end", values=(date, max_t, min_t, day_desc, f"{avg_hum}%"))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"Could not connect to weather service: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
