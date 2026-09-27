import speech_recognition as sr
import pyttsx3
from commands import handle_command
from ai import ask_ai


def speak(text):
    print("Alaska:", text)

    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)

    engine.say(text)
    engine.runAndWait()
    engine.stop()


recognizer = sr.Recognizer()

# Make Alaska wait a little longer before deciding
# that you have stopped speaking.
recognizer.pause_threshold = 1.0
recognizer.non_speaking_duration = 0.5


speak("Hello, I am Alaska. I am ready.")


while True:

    # --------------------------------
    # WAIT FOR WAKE WORD
    # --------------------------------

    try:

        with sr.Microphone(device_index=1) as source:

            print("Listening for Alaska...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

        text = recognizer.recognize_google(audio)

        print("You:", text)

        if "alaska" not in text.lower():

            print("Wake word not detected.")

            continue

    except sr.WaitTimeoutError:

        print("I didn't hear anything.")

        continue

    except sr.UnknownValueError:

        print("I couldn't understand you.")

        continue

    except sr.RequestError:

        speak(
            "There is a problem with the speech recognition service."
        )

        continue


    # --------------------------------
    # WAKE WORD DETECTED
    # --------------------------------

    speak("Yes, how can I help you?")


    # --------------------------------
    # LISTEN FOR COMMAND
    # --------------------------------

    try:

        with sr.Microphone(device_index=1) as source:

            print("Waiting for your command...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=15
            )

        command = recognizer.recognize_google(audio).lower()

        print("Command:", command)


        # --------------------------------
        # NORMAL COMMANDS
        # --------------------------------

        result = handle_command(command, speak)

        if result == "STOP":
           break

        if result is False:

           print("Alaska AI: Thinking...")

           answer = ask_ai(command)

           speak(answer)


    except sr.WaitTimeoutError:

        print("No command received.")

    except sr.UnknownValueError:

        speak("Sorry, I didn't understand that.")

    except sr.RequestError:

        speak(
            "There is a problem with the speech recognition service."
        )

    except Exception as e:

        print("Error:", e)

        speak("Sorry, something went wrong.")