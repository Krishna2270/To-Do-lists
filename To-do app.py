import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# ------------------------------------------------------
# TO-DO LIST APPLICATION
# ------------------------------------------------------
# Features:
# 1. Add Task
# 2. View Tasks
# 3. Update Task
# 4. Mark Task as Completed
# 5. Delete Task
# 6. Save / Load Tasks Automatically
# 7. User-friendly Interface using Tkinter
# ------------------------------------------------------

# File to store tasks
TASK_FILE = "tasks.json"

# List to hold tasks
tasks = []

# ------------------------------------------------------
# Core Functionalities
# ------------------------------------------------------

def load_tasks():
    """Load saved tasks from a JSON file (if exists)."""
    global tasks
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            try:
                tasks = json.load(file)
            except json.JSONDecodeError:
                tasks = []
    refresh_task_list()


def save_tasks():
    """Save all tasks to a JSON file."""
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def add_task():
    """Add a new task to the list."""
    task_name = entry_task.get().strip()
    if not task_name:
        messagebox.showwarning("Input Error", "Please enter a task.")
        return

    tasks.append({"task": task_name, "status": "Pending"})
    entry_task.delete(0, tk.END)
    refresh_task_list()
    save_tasks()


def update_task():
    """Update the selected task."""
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a task to update.")
        return

    index = selected[0]
    current_task = tasks[index]["task"]

    new_task = simpledialog.askstring("Update Task", "Enter updated task:", initialvalue=current_task)
    if new_task:
        tasks[index]["task"] = new_task.strip()
        refresh_task_list()
        save_tasks()


def delete_task():
    """Delete the selected task."""
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a task to delete.")
        return

    index = selected[0]
    confirm = messagebox.askyesno("Confirm Delete", f"Delete task: '{tasks[index]['task']}'?")
    if confirm:
        del tasks[index]
        refresh_task_list()
        save_tasks()


def mark_complete():
    """Mark the selected task as completed."""
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a task to mark complete.")
        return

    index = selected[0]
    tasks[index]["status"] = "Completed"
    refresh_task_list()
    save_tasks()


def refresh_task_list():
    """Refresh the display of the task list."""
    listbox.delete(0, tk.END)
    for t in tasks:
        display = f"{t['task']}   →   [{t['status']}]"
        listbox.insert(tk.END, display)


def clear_all():
    """Clear all tasks from the list."""
    confirm = messagebox.askyesno("Clear All", "Are you sure you want to delete all tasks?")
    if confirm:
        tasks.clear()
        refresh_task_list()
        save_tasks()

# ------------------------------------------------------
# GUI DESIGN
# ------------------------------------------------------

root = tk.Tk()
root.title("📝 To-Do List App")
root.geometry("500x550")
root.resizable(False, False)
root.configure(bg="#f4f4f4")

# Title Label
tk.Label(root, text="📝 To-Do List", font=("Arial", 22, "bold"), bg="#f4f4f4").pack(pady=10)

# Entry Box
entry_task = tk.Entry(root, font=("Arial", 14), width=35, borderwidth=3, relief="ridge")
entry_task.pack(pady=10)

# Button Frame
frame_buttons = tk.Frame(root, bg="#f4f4f4")
frame_buttons.pack(pady=5)

tk.Button(frame_buttons, text="Add Task", width=12, bg="#4CAF50", fg="white", command=add_task).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_buttons, text="Update Task", width=12, bg="#FF9800", fg="white", command=update_task).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_buttons, text="Mark Complete", width=12, bg="#2196F3", fg="white", command=mark_complete).grid(row=0, column=2, padx=5, pady=5)
tk.Button(frame_buttons, text="Delete Task", width=12, bg="#F44336", fg="white", command=delete_task).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_buttons, text="Clear All", width=12, bg="#607D8B", fg="white", command=clear_all).grid(row=1, column=1, padx=5, pady=5)

# Listbox for tasks
listbox = tk.Listbox(root, font=("Arial", 13), width=50, height=15, selectmode=tk.SINGLE)
listbox.pack(pady=10)

# Footer
tk.Label(root, text="© 2025 To-Do List App", bg="#f4f4f4", font=("Arial", 10)).pack(pady=5)

# Load tasks on start
load_tasks()

# Run the application
root.mainloop()
