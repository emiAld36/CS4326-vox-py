####################################################################################################
# FILE: VOX_MAIN.PY
# CREATED BY UKP7 IN 2024
# HUMAN FACTORS GROUP 24
# VOX PYXIS VER 2.0
# VOSK MODEL developed by Alpha Cephei
# 
# THIS CODE BUILDS A SQLITE DATABASE THAT STORES
# TASKS TO BE MANAGED BY THE VOX PYXIS CODE BASE
# THE TASKS WILL BE MANAGABLE ONLY BY VOICE COMMAND
# THE IDEA IS THAT THIS APP WOULD BE AID TO THE BLIND
# OR THE VISUALLY IMPAIRED.
#####################################################################################################

import pyttsx3
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json
from task_database import create_table, add_task, delete_task, update_task, view_tasks, view_tasks_by_category
import numpy
from rapidfuzz import process # this is a fuzzy matching library
#from TTS.api import TTS #THIS IS A HUMAN LIKE VOICE (COMPLEX AND PERFORMANCE TOOK A HIT)


# problem: speech recognition will pick up numbers in their spelled form
# solution: have each number associated with an int for look up
# for testing and demo purposes this solution works but is not scalable.

def words_to_numbers(text):
    ## USE word2number library in an update 
    number_words = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
        "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13", 
        "fourteen": "14", "fifteen": "15", "sixteen": "16", "seventeen": "17", 
        "eighteen": "18", "nineteen": "19", "twenty": "20"
    }
    words = text.split()
    converted = [number_words.get(word, word) for word in words]
    return "".join(converted) #just return the concatenation 

# this is the dictionary for fuzzy matching
valid_commands=[    
    "view tasks",
    "add task",
    "new task",
    "delete task",
    "update task",
    "complete task",
    "I finished a task"
    "exit"
    ]

def match_command(input_command):
    #Match the user command with the closest valid command
    #command, score = process.extractOne(input_command, valid_commands)
    result = process.extractOne(input_command, valid_commands)
    if result:
        best_match, score, _ = result
        return best_match if score > 70 else None
    return None
    #Set a similarity threshold (like 70%) for valid matches
    #return command if score > 70 else None

# Initialize Text-to-Speech engine, in my case pyttsx3
# another option is TTS.api (was a challenge to use, needed alot of pre rendering, still an option though)
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Adjust speech rate if necessary
#setting up default voice
voices = engine.getProperty('voices')
default_voice_id = voices[0].id # this is set to the OG voice

###THIS IS FOR PYTTSx3##############
def speak(text):
    engine.say(text)
    engine.runAndWait()
#################################

# ##THIS IS FOR COQUI TTS##############
# HUMAN LIKE AUDIO BUT INCREASES COMPLEXITY AND PROCESSING
# tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
# def speak(text):
#     """Convert text to speech using Coqui TTS."""
#     tts.tts_to_file(text=text, file_path="output.wav")
#     os.system("start output.wav")  # Play the audio file
# ########################################

def complete_task():
    #Prompts the user to complete a task and removes it from the task list."""
    speak("Which task ID would you like to mark as complete?")
    task_id_text = listen()
    task_id = words_to_numbers(task_id_text)  # Convert spoken words to digits
    print(f"Interpreted Task ID: {task_id}")  # Debugging

    if not task_id.isdigit():  # check if ID is a num
        speak("Invalid task ID.")
        return

    task_id = int(task_id)  # Convert to integer for database operations

    # Confirm the task exists before deleting
    tasks = view_tasks()
    task_to_complete = next((task for task in tasks if task[0] == task_id), None)
    if not task_to_complete:
        speak(f"Task with ID {task_id} does not exist.")
        return

    speak(f"Are you sure you want to complete and remove the task: {task_to_complete[1]}?")
    confirmation = listen()
    if confirmation.lower() in ["yes", "yeah", "confirm"]:
        try:
            delete_task(task_id)  # Remove the task
            speak(f"Task '{task_to_complete[1]}' has been completed and removed.")
        except Exception as e:
            print(f"Error completing task: {e}")
            speak("An error occurred while completing the task. Please try again.")
    else:
        speak("Task completion canceled.")

# Load Vosk model
# CHANGE THIS IF NEEDED WHEN SUBMITTING 1.6gb TO LARGE FOR GIT
MODEL_PATH = "vosk-model-en-us-0.22"  # Path to my Vosk model(.22 is a 1.6gb model)
model = Model(MODEL_PATH)

# this initialzes the VOSK recognizer (provided by vosk)
recognizer = KaldiRecognizer(model, 16000)

# this function uses SoundDevice to capture audio from my device(in chuncks)
def listen():
    # Listen for a command using Vosk and display recognized text.
    # data is pulled in as bytes so we need to actually pass those to be
    # processed, by vosk of course
    speak("waiting...") ##might change this to a sound and only play after a duration
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1) as stream: #this is just set based on vosks requirments 
        print("MIC ACTIVE") ##DEV USE
        while True:
            data, overflowed = stream.read(4000)  # Get the audio data
            if overflowed:
                print("Audio overflow occurred.")
            audio_bytes = bytes(data)  # Convert the buffer object to bytes
            # audio bytes get passed here to be checked
            if recognizer.AcceptWaveform(audio_bytes):  # Pass the bytes to Vosk
                result = json.loads(recognizer.Result())
                print("Recognized text:", result)  # Show full result for debugging
                if "text" in result:
                    recognized_text = result["text"]
                    print(f"Recognized Command: {recognized_text}")  # Display just the text
                    return recognized_text.lower()

def handle_command(command):
    # Use fuzzy matching to find the closest valid command
    matched_command = match_command(command)

    if not matched_command:
        speak("Sorry, I didn't catch that.")
        return

    elif matched_command == "view tasks":
        speak("Do you want to view tasks by category?")
        response = listen()
        confirmation_phrases = ["yes", "yes please", "yeah"]
        if any(phrase in response for phrase in confirmation_phrases):
            speak("Which category?")
            category = listen()
            tasks = view_tasks_by_category(category)
            if tasks:
                speak(f"Here are your tasks in the '{category}' category.")
                for task in tasks:
                    speak(f"Task {task[0]}, {task[1]}.")
            else:
                speak(f"No tasks found in the '{category}' category.")
        else:
            tasks = view_tasks()
            if tasks:
                speak("Here are your tasks.")
                for task in tasks:
                    speak(f"Task ID {task[0]}, {task[1]}.")
            else:
                speak("You have no tasks.")


    elif matched_command == "add task":
        speak("What do you need to do?")
        task_name = listen()
        if not task_name:
            speak("Task name cannot be empty. Please try again.")
            return
        speak("What category should this task belong to?")
        task_category = listen() or "Uncategorized"
        add_task(task_name, task_category)  # No need to specify status
        speak(f"Task '{task_name}' added successfully under the '{task_category}' category with status 'Pending'.")

    elif matched_command == "complete task":
        complete_task()

    elif matched_command == "delete task":
        speak("Which task ID should I delete?")
        task_id_text = listen()
        task_id = words_to_numbers(task_id_text)  # Convert spoken words to digits
        print(f"Interpreted Task ID: {task_id}")  # Debugging
        if not task_id.isdigit():
            speak("Invalid task ID.")
            return
        delete_task(int(task_id))
        speak(f"Task with ID {task_id} deleted successfully.")

    elif matched_command == "update task":
        speak("Which task ID should I update?")
        task_id_text = listen()
        task_id = words_to_numbers(task_id_text)  # convert digit
        print(f"Interpreted Task ID: {task_id}")  # Debugging

        if not task_id.isdigit():
            speak("Invalid task ID.")
            return

        task_id = int(task_id)

        # Ask for new status only
        speak("What is the new status of the task?")
        new_status = listen()
        if not new_status.strip():  # Ensure the status is not empty
            speak("Invalid status. Please try again.")
            return

        # Update the task with the new status
        try:
            update_task(task_id, None, new_status)  # Only pass the status to the update function
            speak(f"Task with ID {task_id} updated to status '{new_status}'.")
        except Exception as e:
            print(f"Error updating task: {e}")
            speak("An error occurred while updating the task. Please try again.")


    elif matched_command == "exit":
        speak("Goodbye!")
        exit(0)



# NEW FEATURE: CHOOSE VOICE
def choose_voice():
    # List of allowed voice indices
    allowed_indices = [14, 19, 29, 38, 51, 66]
    voices = engine.getProperty('voices')  # Fetch all available voices

    # Filter voices based on allowed indices
    filtered_voices = [voices[i] for i in allowed_indices if i < len(voices)]
    if not filtered_voices:
        speak("No available voices match the allowed indices. Using the default voice.")
        engine.setProperty('voice', default_voice_id)
        return

    # Allow the user to choose from the filtered voices
    for index, voice in enumerate(filtered_voices):
        print(f"Voice {index + 1}: {voice.name}")
        engine.setProperty('voice', voice.id)
        speak(f"This is voice {index + 1}.")

    speak("Please choose a voice by saying one, two, three, and so on.")
    choice = listen()
    numeric_choice = words_to_numbers(choice)  # Convert words to numbers

    if numeric_choice.isdigit():
        numeric_choice = int(numeric_choice)
        if 1 <= numeric_choice <= len(filtered_voices):
            selected_voice = filtered_voices[numeric_choice - 1]
            engine.setProperty('voice', selected_voice.id)
            speak(f"Voice {numeric_choice} selected.")
        else:
            speak("Invalid choice. Using the default voice.")
            engine.setProperty('voice', default_voice_id)
    else:
        speak("Invalid input. Using the default voice.")
        engine.setProperty('voice', default_voice_id)




def main():
    # for i in range(0,10,1):
    #     delete_task(task_id=i)
    create_table()

    #user name / initial set up
    choose_voice()
    speak("Initial set up, what would you like to be called?")
    user_name = listen()
    speak("Welcome to Vox Pysis")
    speak(user_name)
    speak("set up complete")
    # Inform the user that they can ask for available commands
    speak("Say 'commands' to hear the available commands.")
    
    while True:
        command = listen()
        if command:
            if "commands" in command:
                speak("You can say 'view tasks', 'add task', 'delete task', 'update task', or 'exit'.")
            else:
                handle_command(command)

if __name__ == "__main__":
    main()
