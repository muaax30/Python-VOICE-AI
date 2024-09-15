import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import pywhatkit
import requests
import datetime
import smtplib
import time
import threading

# Initialize the speech recognition and text-to-speech engines
listener = sr.Recognizer()
engine = pyttsx3.init()

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            status_label.config(text="Listening...")
            root.update()
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'assistant' in command:
                command = command.replace('assistant', '')
                status_label.config(text=f"Command: {command}")
                root.update()
                print(command)
    except Exception as e:
        print(e)
        status_label.config(text="Error: " + str(e))
        return None
    return command

def send_email(to_email, subject, body):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail('your_email@gmail.com', to_email, message)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email. Error: {e}"

def set_alarm(alarm_time):
    def alarm():
        current_time = time.strftime('%H:%M')
        while current_time != alarm_time:
            current_time = time.strftime('%H:%M')
            time.sleep(10)
        talk(f"Wake up! It's {alarm_time}")
        status_label.config(text=f"Alarm ringing! Time: {alarm_time}")

    threading.Thread(target=alarm).start()

def get_weather(city):
    api_key = 'your_openweathermap_api_key'
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if data['cod'] == 200:
        main = data['main']
        temperature = main['temp']
        weather_desc = data['weather'][0]['description']
        return f"The temperature in {city} is {temperature}°C with {weather_desc}."
    else:
        return "Sorry, I couldn't fetch the weather details."

def run_assistant():
    command = take_command()
    if command:
        if 'play' in command:
            song = command.replace('play', '')
            talk('Playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            talk('Current time is ' + current_time)
            status_label.config(text="Current time is " + current_time)
        elif 'weather' in command:
            talk("Which city's weather would you like to know?")
            city = take_command()
            if city:
                weather = get_weather(city)
                talk(weather)
                status_label.config(text=weather)
        elif 'remind me' in command:
            talk("What should I remind you about?")
            reminder = take_command()
            talk(f"Setting a reminder to: {reminder}")
            status_label.config(text=f"Reminder set: {reminder}")
        elif 'send email' in command:
            talk("Who would you like to send the email to?")
            recipient = take_command()
            talk("What is the subject?")
            subject = take_command()
            talk("What would you like to say?")
            body = take_command()
            status = send_email(recipient, subject, body)
            talk(status)
            status_label.config(text=status)
        elif 'set alarm' in command:
            talk("What time should I set the alarm for? Please say it in HH:MM format.")
            alarm_time = take_command()
            set_alarm(alarm_time)
            status_label.config(text=f"Alarm set for {alarm_time}")
        else:
            talk("Sorry, I didn't understand that command.")
            status_label.config(text="Unknown command")

def on_start_click():
    talk("How can I help you today?")
    run_assistant()

# Create GUI with Tkinter
root = tk.Tk()
root.title("Voice Assistant")

# Customizing the background, button styles, and text
root.configure(bg='#282C34')  # Set background color
label = tk.Label(root, text="Voice Assistant", font=("Arial", 24, 'bold'), bg='#282C34', fg='#61AFEF')
label.pack(pady=20)

start_button = tk.Button(root, text="Start", command=on_start_click, font=("Arial", 16), 
                         bg='#98C379', fg='#282C34', activebackground='#61AFEF', activeforeground='white')
start_button.pack(pady=10)

status_label = tk.Label(root, text="Status: Ready", font=("Arial", 14), fg="#E06C75", bg='#282C34')
status_label.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 16), 
                        bg='#E06C75', fg='#282C34', activebackground='#61AFEF', activeforeground='white')
exit_button.pack(pady=10)

root.mainloop()
