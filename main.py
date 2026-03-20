import requests
import speech_recognition as sr
import webbrowser
from gtts import gTTS
import pygame
import os
from musicLib import music
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize engines once at the top
r = sr.Recognizer()

pygame.init()
pygame.mixer.init()

def speak(text):
    # Generate the audio
    tts = gTTS(text=text, lang='en', tld='co.uk')
    filename = "response.mp3"
    tts.save(filename)
    
    # Play the audio
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    # Clean up the file so it doesn't clutter your folder
    pygame.mixer.music.unload()
    os.remove(filename)

def processCommand(command):
    if "open youtube" in command.lower():
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in command.lower():
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
    elif "open linkedin" in command.lower():
        speak("Opening LinkedIn.")
        webbrowser.open("https://www.linkedin.com")
    elif "what is the time" in command.lower():
        from datetime import datetime
        now = datetime.now().strftime("%H:%M")
        speak(f"The current time is {now}.")
    elif command.lower().startswith("play "):
        song= command.split(" ")[1]
        link=music[song]
        webbrowser.open(link)
    elif "news" in command.lower():
        api_key = os.getenv('NEWS_API_KEY').strip()
        print(f"MY KEY IS: {api_key}")
        data=requests.get(f"https://newsapi.org/v2/everything?q=India&language=en&apiKey={api_key}")
        print(f"Response Status Code: {data.status_code}")
        
        if data.status_code==200:
            articles=data.json().get("articles", [])
            print(f"Number of articles received: {len(articles)}")
            
            for article in articles[:5]:  # Read top 5 headlines
                print(article['title'])
                speak(article['title'])
        else:
            print(f"Error Response -> {data.text}")
            speak("I am getting an error from the news server.")
    else:
        speak("Sorry, I didn't understand that command.")
    
if __name__ == "__main__":
    speak("Initializing ARGUS.....")
    
    while True:
        print("\nSay 'ARGUS' to activate the assistant.")
        try:
            with sr.Microphone() as source:
                # 1. Calibrate for background noise (Crucial for accuracy)
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                
                audio = r.listen(source, timeout=5, phrase_time_limit=4)
            
           
            command = r.recognize_google(audio).lower()
            print(f"You said: {command}")
            
            if "argus" in command or "argos" in command:
                print("ARGUS activated.")
                speak("Ya")
                
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening for command...")
                    
                    audio = r.listen(source, timeout=5, phrase_time_limit=4)
                command = r.recognize_google(audio).lower()
                print(f"You said: {command}")
                processCommand(command)

        except sr.WaitTimeoutError:
            pass # Normal behavior when no one is talking
        except sr.UnknownValueError:
            pass # Normal behavior when it hears a noise but no recognizable words
        except sr.RequestError:
            print("Error: Could not connect to Google's servers. Check your internet.")
        except Exception as e:
            print(f"Unexpected Error: {e}")