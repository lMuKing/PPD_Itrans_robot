import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Use the microphone as the audio source
with sr.Microphone() as source:
    print("🎤 Say something:")
    audio = recognizer.listen(source)

try:
    # Recognize speech using Google Web Speech API
    text = recognizer.recognize_google(audio, language="en-US")
    print("You said:", text)

    # Save the result in a string
    my_transcript = text

except sr.UnknownValueError:
    print("Sorry, I could not understand your speech.")
    my_transcript = ""
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
    my_transcript = ""

# Do something with the string
print("Final string saved:", my_transcript)
