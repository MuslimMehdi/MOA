import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pyjokes
import googlesearch
import beautifulsoup4


def speak(text):
    print(f"Assistant: {text}")
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        print("Speech output not supported in Colab.")

def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am MOA Clanker. How can I help you today?")

def take_command():
    return input("You (type your command): ").lower()

def run_assistant():
    wish_user()
    while True:
        query = take_command()

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia:")
                speak(result)
            except:
                speak("Sorry, I couldn't find anything.")

        elif 'open' in query:
            query_list = query.split()
            print("Opening " + query_list[1].capitalize(),"...")
            try:
                # Perform the Google search and get the first result
                first_result = search("Google",query, num=1, stop=1, pause=2)

                # Open the first result in a new browser tab
                print(f"Opening the first search result for '{query}': {first_result}")
                webbrowser.open_new_tab(first_result)

            except StopIteration:
                print(f"No search results found for '{query}'.")


        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {strTime}")

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif 'exit' in query or 'bye' in query:
            speak("Goodbye! Have a nice day!")
            break

        else:
            speak("Sorry, I didn't understand that. Try again.")

run_assistant()