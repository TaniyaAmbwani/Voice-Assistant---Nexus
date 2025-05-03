import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    """Text-to-Speech function"""
    print(f"Speaking: {text}")  # Debugging print
    engine.say(text)
    engine.runAndWait()
    

def processCommand(command):
    """Process voice command for web and music actions"""
    command = command.lower().strip()  # Normalize the command to lowercase
    
    # Handle web commands
    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
    
    # Handle music commands
    elif command.startswith("play"):
        # Capture the song name after the 'play' keyword
        song_name = " ".join(command.split(" ")[1:]).strip().lower()  # Convert to lowercase
        print(f"Requested song name: '{song_name}'")  # Debugging print
        
        # Look for a case-insensitive match in the music library
        for key in musicLibrary.music:
            if key.lower() == song_name:
                song_link = musicLibrary.music[key]
                print(f"Playing song: {key}")  # Debugging print
                webbrowser.open(song_link)  # Open the song in the browser
                return

        # If the song is not found
        speak(f"Sorry, I couldn't find the song '{song_name}'")
        print(f"Song '{song_name}' not found in the music library")  # Debugging print
    
    
    elif "news" in command.lower():
        recognizer = requests.get("#Key")
        
    
        if recognizer.status_code == 200:
            # Parse the JSON response
            data = recognizer.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])


def listen_for_command():
    """Listen for a command after recognizing the wake word"""
    try:
        with sr.Microphone() as source:
            print("Listening for command...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            print(f"Command recognized: {command}")  # Debugging print
            processCommand(command)
    except sr.UnknownValueError:
        print("Sorry, I did not understand the command.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    speak("Initializing Nexus...")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word 'Nexus'...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                word = recognizer.recognize_google(audio)
                
                print(f"Recognized: {word}")  # Added print to check recognition
                
                if word.lower() == "nexus":
                    print("Wake word 'Nexus' detected")  # Debugging print
                    speak("Yes")  # This should speak 'Yes' if the word is recognized
                    # Listen for command after confirmation
                    print("Nexus Active.... Listening for command")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error: {e}")
