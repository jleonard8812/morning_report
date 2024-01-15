import subprocess
import time
from datetime import datetime
from gtts import gTTS
import requests

def get_weather(api_key):
    city = "Durango"
    country_code = "US"
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': f'{city},{country_code}',
        'appid': api_key,
        'units': 'imperial',  
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            temperature = data['main']['temp']
            description = data['weather'][0]['description']

            return f"The current temperature in {city}, {country_code} is {temperature}°C. Weather: {description}."
        else:
            return f"Failed to fetch weather data. Error: {data['message']}"

    except Exception as e:
        return f"An error occurred: {e}"


def get_headlines(api_key):
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        'apiKey': api_key,
        'country': 'us',  
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            # Extract headlines
            articles = data['articles']
            headlines = "\n".join([article['title'] for article in articles])
            return headlines
        else:
            return f"Failed to fetch headlines. Error: {data['message']}"

    except Exception as e:
        return f"An error occurred: {e}"


def create_audio_report(weather_info, headlines_info):
    # Combine weather and headlines into a single report
    report_text = f"{weather_info}\n\n{headlines_info}"

    # Convert the text to speech using gTTS
    tts = gTTS(report_text, lang='en', slow=False)
    
    # Save the audio file
    audio_file_path = '/home/pi/morning_report.mp3'
    tts.save(audio_file_path)

    return audio_file_path

def play_morning_report(file_path):
    # Play the audio file via Bluetooth
    subprocess.run(['sudo', 'systemctl', 'stop', 'bluealsa'])
    subprocess.run(['sudo', 'bluealsa-aplay', '-i', 'hci0', file_path])

if __name__ == "__main__":
    # Replace 'your_openweathermap_api_key' with your actual OpenWeatherMap API key
    weather_api_key = '80c8c37e556e00ffec47b7fc241e302c'
    news_api_key = 'd8028ff6f278447fb23ce6072e632de6'

    # Get weather and headlines
    weather_info = get_weather(weather_api_key)
    headlines_info = get_headlines(news_api_key)

    # Create the audio report
    audio_report_path = create_audio_report(weather_info, headlines_info)

    # Schedule the script to run every day at 7 am using a scheduler
    current_time = datetime.now().strftime("%H:%M")
    if current_time == "07:00":
        # Play the morning report via Bluetooth
        play_morning_report(audio_report_path)
