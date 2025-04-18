from dependencies import *


#-------------------------------------------------------------------------------------------------------------------------#

Model_Running_URL = "http://localhost:11434"
OLLAMA_MODEL = None

def chatbot():
        global OLLAMA_MODEL

        if not check_ollama_server(Model_Running_URL):
            print("Ollama server not running. Please start Ollama and try again.")
            return

        OLLAMA_MODEL = initialize_ollama_model(Model_Running_URL, "llama3:8b")

        if not OLLAMA_MODEL:
            return

        print("🧠 Chatbot (say 'exit' to quit)")
        speak(" Chatbot is ready.")
        while True:
            query = listen()
            if query:
                if query.lower() in ["exit", "quit"]:
                    break
                reply = generate_response(query)
                print(f"Bot: {reply}\n")
                speak(reply)

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
# ---------------------------------------------------------------------------------------------------------------#



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)

driver = None

def open_spotify_app():
    # Open Spotify from the start menu (adjust the command for your OS and setup)
    pyautogui.hotkey('win', 's')  # Open the start menu
    time.sleep(1)
    pyautogui.write('Spotify')  # Type Spotify in the search
    pyautogui.press('enter')  # Open Spotify
    time.sleep(5)  # Wait for Spotify to open
def open_app(query):
    # Open Spotify from the start menu (adjust the command for your OS and setup)
    pyautogui.hotkey('win', 's')  # Open the start menu
    time.sleep(1)
    pyautogui.write(query)  # Type Spotify in the search
    pyautogui.press('enter')  # Open Spotify
    time.sleep(5)  # Wait for Spotify to open

def play_song(song_name):
    # Example function to search and play a song
    # Ensure Spotify is the active window before executing these commands
    pyautogui.hotkey('ctrl', 'l')  # Focus the search bar
    time.sleep(1)
    pyautogui.write(song_name)  # Type the song name
    pyautogui.press('enter')  # Start the search
    time.sleep(2)
    pyautogui.press('enter')  # Select the first result
    time.sleep(1)
    speak('What song would you like to play next?')
    song_query = takeCommand().lower()
    if 'stop' in song_query:
        return
    else:
        speak(f'Searching {song_query} on Spotifi...')
        play_song(song_query)
def byebye():
    print("Bye Bye Sir!")
    speak("Bye Bye Sir!")
    os._exit(1)
def init_driver():
    global driver
    if driver is None:
        driver = webdriver.Chrome()
   
   
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        print("Good Morning!")
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        print("Good Afternoon!")
        speak("Good Afternoon!")  

    else:
        print("Good Evening!")
        speak("Good Evening!")  
    print("I am Jarvis Sir. I am an AI, develoved to automate the tasks. Please tell me how may I asist you")
    speak("I am Jarvis Sir. I am an AI, develoved to automate the tasks. Please tell me how may I asist you")      
def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        speak("Say that again please...")
        return "None"
    return query


def init_driver():
    global driver
    if driver is None:
        driver = webdriver.Chrome()  # Ensure the path to your ChromeDriver is correct

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    engine.setProperty('rate', 200)
def open_youtube_search_and_play(query):
    try:
        init_driver()
        driver.get("https://www.youtube.com")
        time.sleep(2)  # Wait for the page to load

        # Locate the search box and enter the query
        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)  # Wait for the search results to load

        # Locate and click the first video
        first_video = driver.find_element(By.XPATH, '//*[@id="video-title"]')
        first_video.click()

    except Exception as e:
        print("An error occurred:", e)

def main():
    try:
        wishMe()  # Your existing wishMe function
        while True:
            query = takeCommand().lower()  # Your existing takeCommand function

            # Logic for executing tasks based on query
            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'search youtube' in query:
                speak('What should I search on YouTube?')
                search_query = takeCommand().lower()
                speak(f'Searching for {search_query} on YouTube...')
                open_youtube_search_and_play(search_query)
               
            elif 'open google' in query:
                speak('Opening Google...')
                init_driver()
                driver.get("https://www.google.com")

            elif 'open spotify' in query:
                speak('What song would you like to play?')
                song_query = takeCommand().lower()
                speak(f'Searching {song_query} on Spotifi...')
                open_spotify_app()
                play_song(song_query)
               
            elif 'chat with me' in query:
                speak('Switching to Chatbot mode...')
                time.sleep(3)       
                chatbot()
               
            elif 'open app' in query:
                speak('What App would you like to open?')
                query = takeCommand().lower()
                print(f'Opening {query}')
                speak(f'Opening {query}')
                open_app(query)
             
            elif 'play music from my directory' in query:
                music_dir = 'D:\\New folder'
                songs = os.listdir(music_dir)
                print(songs)
                os.startfile(os.path.join(music_dir, songs[0]))

            elif ' what is the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")  
                speak(f"Sir, the time is {strTime}")
            elif 'bye-bye' in query:
                byebye()

    except Exception as e:
        print("An error occurred in the main loop:", e)
    finally:
        if driver is not None:
            driver.quit()  # Ensure the browser closes when the program ends

if __name__ == "__main__":
    main()
