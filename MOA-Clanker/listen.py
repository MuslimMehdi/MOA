import speech_recognition as sr

# Create a Recognizer object
r = sr.Recognizer()

# Use the default microphone as the audio source
with sr.Microphone() as source:
    print("Say something!")
    # Listen for audio input
    audio = r.listen(source)

try:
    # Recognize speech using Google's Web Speech API
    text = r.recognize_google(audio)
    print(f"You said: {text}")
except sr.UnknownValueError:
    print("Speech recognition could not understand audio")
