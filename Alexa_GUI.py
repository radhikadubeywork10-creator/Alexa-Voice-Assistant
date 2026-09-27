import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import os
import threading
import tkinter as tk

# Initialize engines
listener = sr.Recognizer()
engine = pyttsx3.init()

def talk(text):
    status_label.config(text="Alexa: " + text)
    root.update()
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            status_label.config(text="Listening...")
            root.update()
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '').strip()
            return command
    except Exception:
        return ""

def run_alexa():
    command = take_command()
    if command:
        user_box.config(state="normal")
        user_box.insert(tk.END, "You: " + command + "\n")
        user_box.config(state="disabled")
        user_box.see(tk.END)

        # 1. EXIT COMMANDS (Top Priority)
        if 'stop' in command or 'bye' in command or 'exit' in command:
            talk("Goodbye! Have a great day.")
            root.quit()

        # 2. GREETINGS & CASUAL CHAT
        elif 'how are you' in command or 'how is your day' in command:
            talk("I am doing great, thank you for asking! How can I help you today?")

        elif 'hello' in command or 'hey' in command or 'hi' in command:
            talk("Hello! What can I do for you?")

        # 3. DATE & DAY (Checked BEFORE Time)
        elif 'day' in command or 'date' in command:
            today = datetime.datetime.now()
            current_day = today.strftime('%A')
            current_date = today.strftime('%B %d, %Y')
            talk(f"Today is {current_day}, {current_date}.")

        # 4. TIME
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            talk("The current time is " + current_time)

        # 5. OPEN APPLICATIONS
        elif 'open chrome' in command:
            talk("Opening Google Chrome")
            os.system("start chrome")

        elif 'open notepad' in command:
            talk("Opening Notepad")
            os.system("start notepad")

        # 6. YOUTUBE PLAYBACK
        elif 'play' in command:
            song = command.replace('play', '').strip()
            talk("Playing " + song + " on YouTube")
            pywhatkit.playonyt(song)

        # 7. GENERAL KNOWLEDGE & QUESTIONS (Wikipedia / Search)
        elif any(w in command for w in ['who', 'what', 'where', 'when', 'why', 'which', 'how', 'tell me about', 'history']):
            topic = command
            # Remove filler question words
            for w in ['who is', 'what is', 'where is', 'when is', 'why is', 'which is', 'how is', 
                      'who', 'what', 'where', 'when', 'why', 'which', 'how', 'tell me about', 'history of']:
                topic = topic.replace(w, '')
            
            topic = topic.replace('the', '').replace('a', '').strip()

            try:
                info = wikipedia.summary(topic, sentences=1)
                talk(info)
            except Exception:
                talk("Let me search that on Google for you.")
                pywhatkit.search(command)

        # 8. FALLBACK FOR ANYTHING ELSE
        else:
            talk("Let me search that on Google for you.")
            pywhatkit.search(command)

    else:
        status_label.config(text="Ready")

def start_listening_thread():
    threading.Thread(target=run_alexa, daemon=True).start()

# --- GUI Setup ---
root = tk.Tk()
root.title("Alexa Voice Assistant Prototype")
root.geometry("450x520")
root.configure(bg="#1e1e2e")

title_label = tk.Label(root, text="Alexa Voice Assistant", font=("Arial", 18, "bold"), fg="#cdd6f4", bg="#1e1e2e")
title_label.pack(pady=15)

status_label = tk.Label(root, text="Click 'Speak' to start", font=("Arial", 12, "italic"), fg="#a6adc8", bg="#1e1e2e")
status_label.pack(pady=5)

user_box = tk.Text(root, height=12, width=45, font=("Consolas", 10), bg="#313244", fg="#a6e3a1", state="disabled", relief="flat")
user_box.pack(pady=15)

speak_button = tk.Button(
    root, 
    text="🎤 Speak", 
    font=("Arial", 14, "bold"), 
    bg="#89b4fa", 
    fg="#11111b", 
    activebackground="#b4befe", 
    padx=20, 
    pady=10, 
    command=start_listening_thread,
    relief="flat"
)
speak_button.pack(pady=15)

root.mainloop()