Vox Pyxis REDUX - README

Overview

Vox Pyxis is an exploration of accessibility features in development more specifically voice recognition and TTS for the visually impaired. The application works with voice recognition, text-to-speech, and a SQLite database to allow users to create, view, update, and delete tasks.

This video shows vox pyxis compiling and running, allowing me to create the database add a task, update a task and delte a task. It also shows initial set up, do to github restrictions it has no audio

![voxDemo](https://github.com/user-attachments/assets/83ed7ac6-4080-4dbf-9f6b-06e0ae2e69dc)


Features

Voice-Operated Task Management: Add, view, update, and delete tasks using voice commands.
Fuzzy Matching: Ensures commands are interpreted correctly even with minor variations.
    Customizable Voice: Choose from a list of voices during initial setup.
    Task Categorization: Organize tasks into categories for easier management.
    Accessible Feedback: Clear text-to-speech responses for all interactions.


Install Dependencies: (built with python 3.9.6)

    pip install -r requirements.txt

    Download the Vosk Model:
        Download the model from Vosk
        https://alphacephei.com/vosk/models (recommended: vosk-model-en-us-0.22 HOWEVER IS A LARGE FILE >1gb
        USE vosk-model-small-en-us-0.15 for smaller file 40M
        Extract the model and place it in the project directory. Ensure the path in the MODEL_PATH variable of vox_main.py is correct.

Usage

    Run the Application:

    python vox_main.py

    Set Up:
        During the initial setup, choose a voice and specify your preferred name.

    Available Commands:
        "view tasks": View all tasks or tasks by category.
        "add task": Add a new task with a name and optional category.
        "delete task": Remove a task by specifying its ID.
        "update task": Update a task's status by specifying its ID.
        "complete task": Mark a task as completed and remove it.
        "exit": Exit the application.

    Command Help:
        Say "commands" at any time to hear the list of available commands.

Example Interaction

    User: "Add task"
    App: "What do you need to do?"
    User: "Buy groceries"
    App: "What category should this task belong to?"
    User: "Shopping"
    App: "Task 'Buy groceries' added successfully under the 'Shopping' category."

Notes

    Ensure your microphone is working properly.
    The app may not perform optimally in noisy environments.
    For improved performance, consider adjusting the fuzzy matching threshold in the match_command function.

Troubleshooting

    Model not found: Ensure the Vosk model is correctly placed in the project directory and the MODEL_PATH variable is updated.
    Dependencies missing: Run pip install -r requirements.txt to install missing libraries.
    Speech recognition issues: Check your microphone input settings or try a different device.
