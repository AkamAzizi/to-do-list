import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os
from datetime import datetime

TASKS_FILE = "tasks.txt"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return [line.strip().split("|") for line in file.readlines()]

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        for task in tasks:
            file.write("|".join(task) + "\n")

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("750x600")
        self.root.configure(bg="#f4f4f4")

        self.tasks = load_tasks()

        # Frame for Task Entry
        self.frame = tk.Frame(self.root, bg="#f4f4f4")
        self.frame.pack(pady=10)

        self.task_entry = tk.Entry(self.frame, width=30, font=('Arial', 14))
        self.task_entry.pack(side=tk.LEFT, padx=10)

        self.priority_combo = ttk.Combobox(self.frame, values=["High", "Medium", "Low"], state="readonly", width=10)
        self.priority_combo.set("Medium")  # Default value
        self.priority_combo.pack(side=tk.LEFT)

        self.add_task_button = tk.Button(self.frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white", font=('Arial', 12))
        self.add_task_button.pack(side=tk.LEFT)

        self.remove_task_button = tk.Button(self.frame, text="Remove Task", command=self.remove_task, bg="#F44336", fg="white", font=('Arial', 12))
        self.remove_task_button.pack(side=tk.LEFT)

        self.edit_task_button = tk.Button(self.frame, text="Edit Task", command=self.edit_task, bg="#FFC107", fg="white", font=('Arial', 12))
        self.edit_task_button.pack(side=tk.LEFT)

        self.task_listbox = tk.Listbox(self.root, width=70, height=20, font=('Arial', 12), bg="#fff", selectbackground="#a0e0a0")
        self.task_listbox.pack(pady=10)

        self.load_tasks()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)  # Clear the current list
        for task in self.tasks:
            task_display = f"{task[0]} | Priority: {task[1]} | Due: {task[2]}"
            self.task_listbox.insert(tk.END, task_display)

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_combo.get()
        due_date = simpledialog.askstring("Input", "Enter due date (YYYY-MM-DD):")
        if task and due_date:
            try:
                # Validate date format
                datetime.strptime(due_date, "%Y-%m-%d")
                self.tasks.append([task, priority, due_date])
                self.task_listbox.insert(tk.END, f"{task} | Priority: {priority} | Due: {due_date}")
                self.task_entry.delete(0, tk.END)
                save_tasks(self.tasks)
            except ValueError:
                messagebox.showwarning("Warning", "Please enter a valid date in the format YYYY-MM-DD.")
        else:
            messagebox.showwarning("Warning", "Please enter a task and a due date.")

    def remove_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.tasks.pop(selected_task_index)
            self.load_tasks()
            save_tasks(self.tasks)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to remove.")

    def edit_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            current_task = self.tasks[selected_task_index]
            new_task = simpledialog.askstring("Edit Task", "Edit your task:", initialvalue=current_task[0])
            new_priority = simpledialog.askstring("Edit Priority", "Edit task priority (High/Medium/Low):", initialvalue=current_task[1])
            new_due_date = simpledialog.askstring("Edit Due Date", "Edit due date (YYYY-MM-DD):", initialvalue=current_task[2])
            if new_task and new_due_date:
                try:
                    datetime.strptime(new_due_date, "%Y-%m-%d")
                    self.tasks[selected_task_index] = [new_task, new_priority, new_due_date]
                    self.load_tasks()
                    save_tasks(self.tasks)
                except ValueError:
                    messagebox.showwarning("Warning", "Please enter a valid date in the format YYYY-MM-DD.")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to edit.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()

