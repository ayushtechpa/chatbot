import speech_recognition as sr
import pyttsx3
from langchain_ollama import OllamaLLM
import requests

Model_Running_URL = "http://localhost:11434"
OLLAMA_MODEL = None

def check_ollama_server(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama server: {e}")
        return False

def initialize_ollama_model(url, model_name):
    try:
        return OllamaLLM(base_url=url, model=model_name)
    except Exception as e:
        print(f"Error initializing Ollama model: {e}")
        return None

def generate_response(prompt):
    global OLLAMA_MODEL
    if OLLAMA_MODEL:
        try:
            response = OLLAMA_MODEL.invoke(prompt)
            return response
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I encountered an error while generating a response."
    else:
        return "Model not initialized. Please restart the application."

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")  # Adjust language as needed
        print(f"You said: {query}\n")
        return query
    except sr.UnknownValueError:
        print("Sorry, I did not understand. Please try again.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def main():
    global OLLAMA_MODEL
    print("🧠 Voice-Enabled LLaMA3 Chatbot (say 'exit' to quit)")
    speak("Voice-Enabled LLaMA3 Chatbot is ready.")

    if not check_ollama_server(Model_Running_URL):
        print("Ollama server not running. Please start Ollama and try again.")
        return

    OLLAMA_MODEL = initialize_ollama_model(Model_Running_URL, "llama3:8b")

    if not OLLAMA_MODEL:
        return

    while True:
        query = listen()
        if query:
            if query.lower() in ["exit", "quit"]:
                break
            reply = generate_response(query)
            print(f"Bot: {reply}\n")
            speak(reply)

if __name__ == "__main__":
    main()