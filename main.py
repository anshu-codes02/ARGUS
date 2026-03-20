import requests
import speech_recognition as sr
import webbrowser
from gtts import gTTS
import pygame
import os
from musicLib import music
from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv()


r = sr.Recognizer()

pygame.init()
pygame.mixer.init()

def speak(text):
    
    tts = gTTS(text=text, lang='en', tld='co.uk')
    filename = "response.mp3"
    tts.save(filename)
    
    # Play the audio
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
   
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    # Clean up the file
    pygame.mixer.music.unload()
    os.remove(filename)
    
    

client=genai.Client(api_key=os.getenv('GEMINI_API_KEY').strip())

# Function to generate response using Gemini API
def generate_response(prompt):
    try:
        assistant_config=types.GenerateContentConfig(
        system_instruction="You are ARGUS, a smart and helpful AI voice assistant. Always keep your answers extremely brief, conversational, and under 4 sentences.",
        temperature=0.7,
        max_output_tokens=200
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=assistant_config
        )
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response at this time."

# Function to process commands
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
        
        data=requests.get(f"https://newsapi.org/v2/everything?q=India&language=en&apiKey={api_key}")
       
        
        if data.status_code==200:
            articles=data.json().get("articles", [])
            
            for article in articles[:5]:  # Read top 5 headlines
                print(article['title'])
                speak(article['title'])
        else:
            print(f"Error Response -> {data.text}")
            speak("I am getting an error from the news server.")
    else:
        response=generate_response(command)
        print(f"ARGUS: {response}")
        speak(response)
    
if __name__ == "__main__":
    speak("Initializing ARGUS.....")
    
    while True:
        print("\nSay 'ARGUS' to activate the assistant.")
        try:
            with sr.Microphone() as source:
                # Calibrate for background noise (Crucial for accuracy)
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