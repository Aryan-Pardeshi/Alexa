import speech_recognition as sr
import webbrowser
from word2number import w2n
import threading
from gtts import gTTS
from playsound import playsound
import random
import requests
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
import time
import pyautogui
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
import json
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, Git_token, Weather_api, HISTORY_FILE
import requests
from loc import my_location

city = my_location() # Get the user's city location according to their IP address


# Load chat history
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    return []
# Save chat history
def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def speak(text):
    from gtts import gTTS
    tts = gTTS(text)
    tts.save('temp.mp3')
    playsound("temp.mp3") 
    os.remove('temp.mp3')  # Clean up the temporary file


def playMusic(name):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET))
    # Try searching for track
    results = sp.search(q=name, type='track', limit=1)
    tracks = results.get('tracks', {}).get('items', [])
    
    if tracks:
        url = tracks[0]['external_urls']['spotify']
        speak(f"Playing track: {name} on Spotify")
        webbrowser.open(url)

    elif (results := sp.search(q=name, type='playlist', limit=1)) and results.get('playlists', {}).get('items', []):
        url = results['playlists']['items'][0]['external_urls']['spotify']
        speak(f"Opening playlist: {name} on Spotify")
        webbrowser.open(url)

    elif (results := sp.search(q=name, type='album', limit=1)) and results.get('albums', {}).get('items', []):
        url = results['albums']['items'][0]['external_urls']['spotify']
        speak(f"Opening album: {name} on Spotify")
        webbrowser.open(url)

    elif (results := sp.search(q=name, type='artist', limit=1)) and results.get('artists', {}).get('items', []):
        url = results['artists']['items'][0]['external_urls']['spotify']
        speak(f"Opening artist: {name} on Spotify")
        webbrowser.open(url)

    else:
        speak("Sorry, I couldn't find anything related to that on Spotify.")

def get_current_time():
    current_time = time.strftime("%I:%M %p")
    return f"The current time is {current_time}"

def aiProcess(command):
    chat_history = load_history()
    messages=[
            SystemMessage("You are Alexa, a smart and helpful girl assistant. Keep your answers short, smart, and friendly. Never sound robotic. If the user says something dumb, roast them playfully like a best friend would. Dont crossquestion the user input, just respond to it. If Alexa is not able to perform a task, she will say Sorry, I am not able to perform that task right now. Dont use emoji in your responses. Make sure that u do not remember the name of the user, just call them 'user' or 'you'."),
            
        ]
    for m in chat_history:
        if m["role"] == "user":
            messages.append(UserMessage(content=m["content"]))
        elif m["role"] == "assistant":
            messages.append(AssistantMessage(content=m["content"]))
    messages.append(UserMessage(content=command))


    endpoint = "https://models.github.ai/inference"
    model = "openai/gpt-4.1-mini"
    token = Git_token  
    

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    response = client.complete(
        messages=messages,
        temperature=1,
        top_p=1,
        model=model
    )
    reply = response.choices[0].message.content
    chat_history.append({"role": "user", "content": command})
    chat_history.append({"role": "assistant", "content": reply})
    if len(chat_history) > 100:
        chat_history = chat_history[-100:]
    save_history(chat_history)

    return reply

def get_weather(city):
    api_key = Weather_api
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url)
        data = res.json()

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        weather_info = f"The temperature in {city} is {temp}°C and the weather is {desc}"
        return weather_info
    except Exception as e:
        return "Sorry, I couldn't fetch the weather information right now"
    
def ai_code_writer(prompt):
    # Use Azure OpenAI client for code generation
    speak("Writing the code for you. The code will be saved in a text file.")

    endpoint = "https://models.github.ai/inference"
    model = "openai/gpt-4.1"
    token = Git_token  


    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    response = client.complete(
        messages=[
            SystemMessage(
                "You are a helpful assistant that writes Python code for the user's request. "
                "Output ONLY the code, with no explanations, no markdown, and no extra text. "
                "Do not say anything except the code."
            ),
            UserMessage(f"Write a Python program for the following request:\n{prompt}"),
        ],
        temperature=0.3,
        top_p=1,
        model=model,
        max_tokens=512
    )

    code = response.choices[0].message.content

    print("Generated Code:\n", code)

    # Save the code to a file
    if not os.path.exists("GeneratedCode"):
        os.mkdir("GeneratedCode")

    filename = f"GeneratedCode/{'_'.join(prompt.split())[:40]}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

    speak("Code written and saved successfully in a text file.")



def reminder_thread(text, delay_seconds):
    time.sleep(delay_seconds)
    speak(f"Reminder: {text}")

def set_reminder(text, delay_seconds):
    speak(f"Reminder set for {delay_seconds // 60} minutes from now.")
    t = threading.Thread(target=reminder_thread, args=(text, delay_seconds))
    t.start()


    
def processCommand(command):
    print(command)
    if "open google" in command.lower():
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command.lower():
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open stack overflow" in command.lower():
        speak("Opening Stack Overflow")
        webbrowser.open("https://stackoverflow.com")
    elif "open github" in command.lower():
        speak("Opening GitHub")
        webbrowser.open("https://github.com")
    elif "open facebook" in command.lower():
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif "open twitter" in command.lower():
        speak("Opening Twitter")
        webbrowser.open("https://twitter.com")
    elif "open instagram" in command.lower():
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
    elif "open linkedin" in command.lower():
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")
    elif "open settings".lower() in command.lower():
        os.system("start ms-settings:")
    elif "write a program" in command.lower() or "code" in command.lower():
        ai_code_writer(command)

    elif "search" in command.lower():
        speak("Searching on Google")
        command = command.lower().replace("search", "").strip()
        command = command.replace(" ", "+")  # Replace spaces with '+' for URL encoding
        webbrowser.open(f"https://www.google.com/search?q={command}")
    
    elif "search youtube" in command.lower():
        speak("Searching on YouTube")
        command = command.lower().replace("search youtube", "").strip()
        command = command.replace(" ", "+")
        webbrowser.open(f"https://www.youtube.com/results?search_query={command}")
    
    
    # elif command.lower().startswith("play"):
    #     song = command.lower().split(" ")[1]
    #     link = musicLibrary.music[song]
    #     command = command.lower().replace("play", "").strip()
    #     if link:
    #         speak(f"Playing {command}")
    #         webbrowser.open(link)
    #     else:
    #         speak("Sorry, I don't have that song in my library.")
    elif command.lower().startswith("play") or ("music" in command.lower()) or ("song" in command.lower()):
        playMusic(command.lower().replace("play", "").replace("music", "").replace("song", "").strip())
    
    elif "play music" in command.lower():
        speak("Can you please tell me the name of the song or artist you want to play?")
    elif "open spotify" in command.lower():
        speak("Opening Spotify")
        webbrowser.open("https://open.spotify.com")
        
    elif "shutdown" in command.lower():
        speak("Do you really want to shut down the computer?, if yes, say 'yes' to confirm")
        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening for confirmation...")
                audio = r.listen(source, timeout=5, phrase_time_limit=15)
                try:
                    confirmation = r.recognize_google(audio).lower()
                    if "yes" in confirmation:
                        speak("Shutting down the computer")
                        os.system("shutdown /s /t 1")
                        break
                    elif "no" in confirmation:
                        speak("Shutdown cancelled")
                        break
                    else:
                        speak("Please say 'yes' to confirm shutdown or 'no' to cancel.")
                except sr.UnknownValueError:
                    speak("I didn't understand that. Please say 'yes' to confirm shutdown or 'no' to cancel.")
    elif "restart" in command.lower():
        speak("Do you really want to restart the computer?, if yes, say 'yes' to confirm")
        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening for confirmation...")
                audio = r.listen(source, timeout=5, phrase_time_limit=15)
                try:
                    confirmation = r.recognize_google(audio).lower()
                    if "yes" in confirmation:
                        speak("Restarting the computer")
                        os.system("shutdown /r /t 1")
                        break
                    elif "no" in confirmation:
                        speak("Restart cancelled")
                        break
                    else:
                        speak("Please say 'yes' to confirm restart or 'no' to cancel.")
                except sr.UnknownValueError:
                    speak("I didn't understand that. Please say 'yes' to confirm restart or 'no' to cancel.")

    elif "open chat gpt" in command.lower():
        speak("Opening Chat GPT")
    elif "time" in command.lower():
        speak(get_current_time())
    elif "weather" in command.lower():
        speak("Fetching the weather information for you.")
        playsound("thinking.mp3")
        weather_info = get_weather(city)
        speak(weather_info)
    

    elif "remind" in command.lower():
        # Always clean and extract the part after "remind"
        command = command.lower().split("remind", 1)[1].strip()
        # Optional cleanup: remove "me to" if it exists
        command = command.replace("me", "").strip()
        while True:
            speak("In how many minutes should I remind you?")
            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Listening for reminder time...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=15)
                    reminder_time = r.recognize_google(audio)
                    reminder_time = reminder_time.lower().replace("in", "").replace("minutes", "").replace("minute","").strip()
                    time_in_minutes = w2n.word_to_num(reminder_time)
                    print("You said:", reminder_time)
                    if time_in_minutes < 0:
                        speak("Please tell me a positive number of minutes.")
                        continue
                delay_seconds = time_in_minutes * 60

                # Launch reminder thread
                threading.Thread(target=reminder_thread, args=(command, delay_seconds)).start()
                speak(f"Okay, I will remind you to {command} in {time_in_minutes} minutes.")
                break
            except Exception as e:
                print("Error:", e)
                speak("I didn't understand that. Please tell me the reminder time in minutes again. like '10")

    elif "stop" in command.lower():
        speak("Stopping all operations. Goodbye!")
        playsound("end.mp3")
        exit(0)
    elif "flip" in command.lower() and "coin" in command.lower():
        speak("Flipping a coin for you...")
        speak(random.choice(["Heads", "Tails"]))
    elif "roll" in command.lower() and "dice" in command.lower():
        speak("Rolling a dice for you...")
        die_num = str(random.randint(1, 6))
        speak(die_num, "is the number on the dice")
        print("Rolled a dice:", die_num)
    elif "screenshot" in command.lower():
        speak("Taking a screenshot...")
        screenshot = pyautogui.screenshot()
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        screenshot.save(f"{formatted_time}.png")
        speak("Screenshot saved successfully.")
    elif "open" in command.lower():
        command = command.lower().replace("open", "").strip()
        command = command.replace(" ", "+")  # Replace spaces with '+' for URL encoding
        speak(f"Opening {command} in your default browser")
        webbrowser.open(f"https://www.google.com/search?q={command}")
    elif "ip address" in command.lower():
        speak("Fetching your IP address...")
        try:
            ip_address = requests.get('https://api.ipify.org').text
            speak(f"Your IP address is {ip_address}")
        except requests.RequestException as e:
            speak("Sorry, I couldn't fetch your IP address right now.")
            print("Error fetching IP address:", e)

    else:
        playsound("thinking.mp3")
        output = aiProcess(command)
        speak(output)
        print("AI Response:", output)
    # else:
    #     speak("Showing results on Google")
    #     command = command.lower().replace("search", "").strip()
    #     command = command.replace(" ", "+")  # Replace spaces with '+' for URL encoding
    #     webbrowser.open(f"https://www.google.com/search?q={command}")
    
    

def standalone_listener_loop():
    playsound("start.mp3")
    while True:
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
                word = r.recognize_google(audio)
            if word.lower() == "alexa":
                playsound("wake.mp3")
                with sr.Microphone() as source:
                    print("Alexa Active...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=15)
                    command = r.recognize_google(audio)
                playsound("end.mp3")
                processCommand(command)
        except Exception as e:
            print("Error: {0}".format(e))

if __name__ == "__main__":
    standalone_listener_loop()