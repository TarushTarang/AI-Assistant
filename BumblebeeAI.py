import random
import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import datetime
import openai
import wikipediaapi
import wikipedia
import list
import time
import pvporcupine
import pyaudio
import struct
import threading


def say(text):
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  


#Voice speed rate
    engine.setProperty('rate', 120)
    engine.setProperty('volume', 0.8)

    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #r.pause_threshold = 0.5
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio.")
            return "Sorry, I did not understand the audio."
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return "Could not request results"
        return query

def ask_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        print(summary)
        say(summary)
    except wikipedia.exceptions.PageError:
        print("Sorry, I couldn't find anything on that topic.")
        say("Sorry, I couldn't find anything on that topic.")
    except Exception as e:
        print(f"An error occurred: {e}")
        say("Sorry, something went wrong.")

def greet_user():
    hour = int(datetime.datetime.now().strftime('%H'))
    if 4 <= hour < 12:
        say("Good morning! I am Bumblebee, your virtual assistant.")
    elif 12 <= hour < 18:
        say("Good afternoon! I am Bumblebee, your virtual assistant.")
    else:
        say("Good evening! I am Bumblebee, your virtual assistant.")

def tell_joke():
    jokes = list.jokes
    joke = random.choice(jokes)
    print(joke)
    say(joke)

def set_reminder(reminder_time, message = "Nothing"):
    say(f"Reminder set for {reminder_time} seconds from now")
    time.sleep(reminder_time)
    say(f"Reminder: {message}")

def wake_word_listener():
    access_key = "8f2Yaoqf3ufmG+YCAiyvAEx3HcGwlYXXrBVr7hMgHPiz4QxU5NuKBQ=="
    porcupine = pvporcupine.create(access_key=access_key, keywords=["bumblebee"])

    pa = pyaudio.PyAudio()

    stream = pa.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
    print("Listening for wake word.....")

    while True:
        pcm = stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        if porcupine.process(pcm) >= 0:
            print("Wake word detected!")
            say("Yes? How can I assist you?")
            handle_commands()

def handle_commands():
        query = takeCommand()
        websites = list.websites

# loop terminating condition
        if "stop" in query.lower():
            say("Good Bye...")
            exit()

# Open websites
        for site in websites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}....")
                webbrowser.open(site[1])

# Ask questions
        if "question" in query.lower():
            say("What do you want to ask?")
            question = takeCommand()
            if question:
                ask_wikipedia(question)
                
# Open whatsapp
        elif "open whatsapp" in query.lower():
            whatsapp_path = r"C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2440.9.0_x64__cv1g1gvanyjgm\WhatsApp.exe"
            if os.path.exists(whatsapp_path):
                say("Opening WhatsApp...")
                os.startfile(whatsapp_path)
            else:
                say("WhatsApp is not installed or the path is incorrect.")

# Play music from youtube
        elif "play song" in query:
            song = query.replace("play song", "").strip()
            webbrowser.open(f"https://music.youtube.com/search?q={song}")
            say(f"Playing {song} on YouTube Music.")
        
# Tell time
        elif "time" in query.lower():
            hour = datetime.datetime.now().strftime("%I")  # 12-hour format
            minute = datetime.datetime.now().strftime("%M")
            period = datetime.datetime.now().strftime("%p")  # AM/PM
            say(f"The time is {hour}:{minute} {period}")

# Tell father's name
        elif "who is your father".lower() in query.lower():
            say("Tarush is my Father, He made me on october 23rd 2023.")

# Ask a joke
        elif "tell me a joke" in query.lower():
            tell_joke()

# Ask to shutdown my laptop
        elif "shut down my laptop" in query.lower():
            say("Shutting down the system.")
            os.system("shutdown /s /t 5")

# Ask to restart my laptop
        elif "restart my laptop" in query.lower():
            say("Restarting the system.")
            os.system("shutdown /r /t 5")

# Setting a reaminder
        elif "set a reminder" in query.lower():
            say("How many seconds from now?")
            reminder_time = int(takeCommand().split()[0])
            say("What should I remind you of?")
            message = takeCommand()
            set_reminder(reminder_time, message)
            say("Setting a reminder.....")

# Just for fun Replay to fuck you
        elif "fuck you" in query.lower():
            say("Shut the fuck up you mother fucker.")

def start_assistant():
    wake_thread = threading.Thread(target=wake_word_listener)
    wake_thread.start()

if __name__ == '__main__':

    greet_user()
    start_assistant()