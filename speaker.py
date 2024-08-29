import wikipedia
import webbrowser
import datetime
import subprocess
import os
import pyttsx3
import speech_recognition as sr
import cv2
from mtcnn import MTCNN
import threading

recognizer = sr.Recognizer()
engine = pyttsx3.init()

#  speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# recognize speech
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio).lower()
            print("You said:", query)
            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't get that.")
            return ""
        except sr.RequestError as e:
            print("Sorry, could not request results; {0}".format(e))
            return ""

def decrease_brightness():
    subprocess.run(["xrandr", "--output", "eDP-1", "--brightness", "1.0"])  
    print("Brightness decreased")

def search_wikipedia(query=""):
    try:
        wikiPage = wikipedia.page(query)
        print(wikiPage.title)
        wikiSummary = wikiPage.summary
        return wikiSummary
    except wikipedia.DisambiguationError as e:
        options = e.options
        if options:
            wikiPage = wikipedia.page(options[0])
            print(wikiPage.title)
            wikiSummary = wikiPage.summary
            return wikiSummary
        else:
            print("No Wikipedia result for", query)
            return "No Wikipedia result"
    except wikipedia.PageError:
        print("No Wikipedia page found for", query)
        return "No Wikipedia page found"

def process_command(query):
    if "open Google" in query:
        webbrowser.open("https://www.google.com")
    elif "open YouTube" in query:
        webbrowser.open("https://www.youtube.com")
    elif "what's the time" in query:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak("It's " + current_time)
    elif "search" in query:
        search_query = query.replace("search", "").strip()
        webbrowser.open("https://www.google.com/search?q=" + search_query)
    elif "open file" in query:
        file_path = "path/to/your/file.txt"  
        try:
            os.startfile(file_path)
        except OSError as e:
            print("Error:", e)
            speak("Sorry, I couldn't open the file.")
    elif "open whatsapp" in query:
        webbrowser.open("https://web.whatsapp.com/")
    elif "open spotify "in query:
        webbrowser.open("https://spotify.com")
    elif "open chatgpt" in query:
        webbrowser.open("https://chat.openai.com/")
    elif "decrease_brightness" in query:
        decrease_brightness()
    elif query.startswith('wikipedia'):
        query = query[10:].strip()
        speak("Querying the universal database")
        speak(search_wikipedia(query))
    elif "exit" in query:
        speak("bye")
        exit()
    else:
        speak("Sorry, I can't do that.")

def face_recognition():
    # Initialize the MTCNN detector
    detector = MTCNN()

    # Start video capture
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert frame to RGB (MTCNN uses RGB format)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the frame
        faces = detector.detect_faces(rgb_frame)

        # Draw rectangles around the faces
        for face in faces:
            x, y, w, h = face['box']
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Display the resulting frame
        cv2.imshow('Face Recognition', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

def main():
    speak("Hello! How can I assist you?")
    
    # Start face recognition in a separate thread
    face_thread = threading.Thread(target=face_recognition)
    face_thread.start()

    while True:
        query = listen()
        if query:
            process_command(query)

if __name__ == "__main__":
    main()
