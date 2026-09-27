import datetime
import os
import webbrowser
import requests
from urllib.parse import quote


def handle_command(command, speak):

    if "stop" in command or "exit" in command or "quit" in command:
        speak("Goodbye. Shutting down.")
        return "STOP"

    elif "hello" in command:
        speak("Hello! How can I help you?")
        return True

    elif "your name" in command:
        speak("My name is Alaska.")
        return True

    elif "my name is" in command:
        name = command.replace("my name is", "").strip()

        if name:
            speak("Nice to meet you, " + name + ".")

        return True

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak("The current time is " + current_time)
        return True

    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak("Today's date is " + current_date)
        return True

    elif "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
        return True

    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
        return True

    elif "open instagram" in command:
        speak("Opening Instagram.")
        webbrowser.open("https://www.instagram.com")
        return True

    elif "search google for" in command:
        query = command.replace("search google for", "").strip()

        if query:
            speak("Searching Google for " + query)
            webbrowser.open(
                "https://www.google.com/search?q=" + quote(query)
            )

        return True

    elif "search youtube for" in command:
        query = command.replace("search youtube for", "").strip()

        if query:
            speak("Searching YouTube for " + query)
            webbrowser.open(
                "https://www.youtube.com/results?search_query="
                + quote(query)
            )

        return True

    elif "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()

        if query:
            speak("Searching Wikipedia for " + query)

            try:
                title = quote(query.replace(" ", "_"))

                url = (
                    "https://en.wikipedia.org/api/rest_v1/page/summary/"
                    + title
                )

                headers = {
                    "User-Agent": "AlaskaVoiceAssistant/1.0"
                }

                response = requests.get(
                    url,
                    headers=headers,
                    timeout=10
                )

                if response.status_code == 200:
                    data = response.json()
                    result = data.get("extract")

                    if result:
                        speak(result)
                    else:
                        speak(
                            "I couldn't find a summary for that topic."
                        )
                else:
                    speak(
                        "I couldn't find that topic on Wikipedia."
                    )

            except requests.exceptions.RequestException:
                speak("I couldn't connect to Wikipedia.")

            except Exception:
                speak(
                    "Something went wrong while searching Wikipedia."
                )

        return True

    elif "open notepad" in command:
        speak("Opening Notepad.")
        os.system("notepad.exe")
        return True

    elif "open calculator" in command:
        speak("Opening Calculator.")
        os.system("start calc")
        return True

    elif "open vs code" in command:
        speak("Opening Visual Studio Code.")
        os.system("code")
        return True

    else:
        # This is important.
        # Unknown commands go to the AI.
        return False