import os
from dotenv import load_dotenv
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import playsound
import time

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.0-flash")  # Fallback model

def generate(command):
    prompt = command

    try:
        response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        print("⚠️ Error:", e)
        return None
    

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Say something:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="en-US")
        print("🗣️ You said:", text)
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand your speech.")
        return ""
    except sr.RequestError as e:
        print(f"❌ Speech recognition service error: {e}")
        return ""
    

def speak2(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)


    engine.say(text)
    engine.runAndWait()



def speak(text):
    filename = f"temp_audio_{int(time.time())}.mp3"
    try:
        tts = gTTS(text, lang='en')
        tts.save(filename)
        playsound.playsound(filename)
    finally:
        if os.path.exists(filename):
            os.remove(filename)


def custom_override(cmd):
    cmd = cmd.lower()

    # If it's an exact match, let Gemini answer
    if cmd.strip() in ["who made you", "present yourself"]:
        return None  # no override → go to Gemini

    # Fuzzy matching
    if any(kw in cmd for kw in ["who built you", "who created you", "who programmed you"]):
        return "Khaled Benchikha, my sir."

    if any(kw in cmd for kw in ["introduce yourself", "show yourself", "are you a robot"]):
        return "I am a smart robot."

    return None  # no match


def main():
    print("🤖 Voice Bot (say 'exit' to quit)")

    while True:
        cmd = recognize_speech()
        if not cmd:
            continue

        if "exit" in cmd.lower():
            speak("Goodbye!")
            break

        # ✨ Check for override
        override = custom_override(cmd)
        if override is not None:
            response = override
        else:
            # Use Gemini for full answer
            response = generate(cmd)

        print("🦾 Response:", response)
        speak(response)


if __name__ == "__main__":
    main()
