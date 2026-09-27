import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia

listener = sr.Recognizer()
engine = pyttsx3.init()

def talk(text):
    print("Alexa:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("\nListening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
            return command
    except Exception as e:
        return ""

def run_alexa():
    command = take_command()
    if command:
        print("You said:", command)
        
        if 'play' in command:
            song = command.replace('play', '')
            talk('Playing ' + song)
            pywhatkit.playonyt(song)
            
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('The current time is ' + time)
            
        elif 'who is' in command or 'what is' in command:
            person = command.replace('who is', '').replace('what is', '')
            info = wikipedia.summary(person, sentences=1)
            talk(info)
            
        elif 'stop' in command or 'bye' in command:
            talk('Goodbye! Have a great day.')
            return False
            
        else:
            talk('I heard you say ' + command)
            
    return True

# Continuous Loop
talk("Hello! How can I help you today?")
while True:
    should_continue = run_alexa()
    if should_continue == False:
        break