####################################################################################################
# FILE: task_database.py
# CREATED BY UKP7 IN 2024
# HUMAN FACTORS GROUP 24
# VOX PYXIS VER 2.0
# THIS CODE HANDLES PYTHON TO SQL COMMUNICATION 
# CURSOR IS USED TO BRIDGE THAT CONNECTION.
#####################################################################################################
import sqlite3

DATABASE_NAME = "tasks.db"


def view_tasks_by_category(category):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute('SELECT task_id, task_name, task_status FROM tasks WHERE task_category = ?', (category,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def create_table():
    """Create the tasks table if it doesn't exist, including a category field."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        task_status TEXT NOT NULL CHECK (task_status IN ('Completed', 'In progress')),
        task_category TEXT DEFAULT 'Uncategorized'
    )
    ''')
    conn.commit()
    conn.close()

def add_task(name, category, status="Pending"):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (task_name, task_status, task_category) VALUES (?, ?, ?)', (name, status, category))
    conn.commit()
    conn.close()




def delete_task(task_id):
    """Delete a task by its ID."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM tasks
    WHERE task_id = ?
    ''', (task_id,))
    conn.commit()
    conn.close()

def update_task(task_id, new_name=None, new_status=None):
    """Update a task's name, status, or both."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    if new_name and new_status:
        cursor.execute('''
        UPDATE tasks
        SET task_name = ?, task_status = ?
        WHERE task_id = ?
        ''', (new_name, new_status, task_id))
    elif new_name:
        cursor.execute('''
        UPDATE tasks
        SET task_name = ?
        WHERE task_id = ?
        ''', (new_name, task_id))
    elif new_status:
        cursor.execute('''
        UPDATE tasks
        SET task_status = ?
        WHERE task_id = ?
        ''', (new_status, task_id))
    conn.commit()
    conn.close()

def view_tasks():
    """View all tasks in the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM tasks
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows
view_tasks()

## field add after table creating so needed its own sql statement 
def add_category_column():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute('''
    ALTER TABLE tasks ADD COLUMN task_category TEXT DEFAULT 'Uncategorized'
    ''')
    conn.commit()
    conn.close()

def reset_task_id_sequence():
    """Reset the AUTOINCREMENT sequence for the tasks table."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'tasks';")
        conn.commit()
        print("Task ID sequence reset successfully.")
    except sqlite3.OperationalError as e:
        print(f"Error resetting sequence: {e}")
    finally:
        conn.close()



# DEV CRAP
# Ensure the database and table are set up
#create_table()

# #List of tasks to add
# tasks = [
#     ("Watch 'Shrek'", "Movies"),
#     ("Watch Shrek part two", "Movies"),
#     ("Write notes for class", "Notes"),
#     ("Write a song", "Writing"),
#     ("Watch 'The Dark Knight' and 'Joker'", "Moivies"),
# ]

# # Add tasks to the database
# for task_name, category in tasks:
#     add_task(task_name, category)  # Default status is 'Pending'

# print("Tasks added successfully!")


##comment out!!
# add_category_column()
# print("Added task_category column.")


## RESET THE DATABASE WITH THESE
# for i in range(0,100,1):
#     delete_task(i)
# reset_task_id_sequence()