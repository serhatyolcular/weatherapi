import requests
import json
from datetime import datetime
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
import ttkthemes

def get_weather(city):
    # We'll use OpenWeatherMap API
    api_key = "YOUR_API_KEY"  # API key obtained from OpenWeatherMap
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    try:
        # Parameters for API request
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric',
            'lang': 'en'
        }
        
        response = requests.get(base_url, params=params)
        weather_data = response.json()
        
        if response.status_code == 404:
            return "City not found!"
            
        if response.status_code != 200:
            return "Could not get weather information!"
        
        return weather_data
        
    except Exception as e:
        return f"An error occurred: {str(e)}"

def create_weather_app():
    root = ttkthemes.ThemedTk()
    root.set_theme("arc")  # Apply a modern theme
    root.title("Weather Application")
    root.geometry("500x600")
    root.configure(bg='#f0f0f0')
    
    # Main frame
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Title
    title_label = ttk.Label(
        main_frame,
        text="Weather Forecast",
        font=("Helvetica", 24, "bold")
    )
    title_label.pack(pady=10)
    
    # Search section
    search_frame = ttk.Frame(main_frame)
    search_frame.pack(fill=tk.X, pady=10)
    
    city_entry = ttk.Entry(
        search_frame,
        font=("Helvetica", 12),
        width=30
    )
    city_entry.pack(side=tk.LEFT, padx=5)
    
    # Digital display frame
    display_frame = ttk.Frame(main_frame)
    display_frame.pack(fill=tk.BOTH, expand=True, pady=20)
    
    # Digital display labels
    city_label = ttk.Label(
        display_frame,
        text="--",
        font=("Digital-7", 28, "bold")
    )
    city_label.pack(pady=5)
    
    temp_label = ttk.Label(
        display_frame,
        text="--°C",
        font=("Digital-7", 46, "bold")
    )
    temp_label.pack(pady=5)
    
    desc_label = ttk.Label(
        display_frame,
        text="--",
        font=("Digital-7", 20)
    )
    desc_label.pack(pady=5)
    
    humidity_label = ttk.Label(
        display_frame,
        text="Humidity: --%",
        font=("Digital-7", 18)
    )
    humidity_label.pack(pady=5)
    
    wind_label = ttk.Label(
        display_frame,
        text="Wind: -- km/h",
        font=("Digital-7", 18)
    )
    wind_label.pack(pady=5)
    
    date_label = ttk.Label(
        display_frame,
        text=datetime.now().strftime('%Y-%m-%d'),
        font=("Digital-7", 16)
    )
    date_label.pack(pady=5)
    
    def update_display(weather_data):
        if isinstance(weather_data, str):  # If it's an error message
            city_label.config(text="Error")
            temp_label.config(text="--°C")
            desc_label.config(text=weather_data)
            humidity_label.config(text="Humidity: --%")
            wind_label.config(text="Wind: -- km/h")
            return
            
        city_label.config(text=weather_data['name'])
        temp_label.config(text=f"{round(weather_data['main']['temp'], 1)}°C")
        desc_label.config(text=weather_data['weather'][0]['description'].title())
        humidity_label.config(text=f"Humidity: {weather_data['main']['humidity']}%")
        wind_label.config(text=f"Wind: {round(weather_data['wind']['speed'] * 3.6, 1)} km/h")
        date_label.config(text=datetime.now().strftime('%Y-%m-%d'))
    
    def show_weather():
        city = city_entry.get()
        weather_data = get_weather(city)
        update_display(weather_data)
    
    search_button = ttk.Button(
        search_frame,
        text="Search",
        command=show_weather
    )
    search_button.pack(side=tk.LEFT, padx=5)
    
    # Also search when Enter key is pressed
    city_entry.bind('<Return>', lambda event: show_weather())
    
    root.mainloop()

if __name__ == "__main__":
    create_weather_app()
