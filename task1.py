import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3 as sql


class TaskManager:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List")
        self.master.geometry("600x400")
        self.master.resizable(0, 0)

        self.connection = sql.connect('tasks.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                priority TEXT,
                                due_date TEXT,
                                completed INTEGER DEFAULT 0
                            )''')
        self.tasks = []

        self.frame = tk.Frame(master, bg="#E6E6E6")
        self.frame.pack(expand=True, fill='both')

        self.title_label = ttk.Label(self.frame, text="To-Do List Project", font=("Arial", 16, "bold"), background="#4CAF50",
                                     foreground="white")
        self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        self.task_label = ttk.Label(self.frame, text="Task:", background="#E6E6E6", font=("Arial", 12))
        self.task_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.task_entry = ttk.Entry(self.frame, width=40)
        self.task_entry.grid(row=1, column=1, padx=10, pady=5)

        self.priority_label = ttk.Label(self.frame, text="Priority:", background="#E6E6E6", font=("Arial", 12))
        self.priority_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.priority_combo = ttk.Combobox(self.frame, values=['High', 'Medium', 'Low'], width=37)
        self.priority_combo.grid(row=2, column=1, padx=10, pady=5)

        self.due_date_label = ttk.Label(self.frame, text="Due Date:", background="#E6E6E6", font=("Arial", 12))
        self.due_date_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.due_date_entry = ttk.Entry(self.frame, width=40)
        self.due_date_entry.grid(row=3, column=1, padx=10, pady=5)

        self.add_button = ttk.Button(self.frame, text="Add Task", command=self.add_task, style="AddButton.TButton")
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.task_frame = ttk.Frame(self.frame)
        self.task_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.retrieve_tasks()
        self.update_task_list()

    def add_task(self):
        title = self.task_entry.get().strip()
        priority = self.priority_combo.get().strip()
        due_date = self.due_date_entry.get().strip()

        if title:
            self.cursor.execute('''INSERT INTO tasks (title, priority, due_date) VALUES (?, ?, ?)''',
                                (title, priority, due_date))
            self.connection.commit()
            self.retrieve_tasks()
            self.update_task_list()
            self.task_entry.delete(0, 'end')
            self.priority_combo.set('')
            self.due_date_entry.delete(0, 'end')
        else:
            messagebox.showwarning("Warning", "Task title cannot be empty!")

    def delete_task(self, task_id):
        response = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?")
        if response:
            self.cursor.execute('''DELETE FROM tasks WHERE id=?''', (task_id,))
            self.connection.commit()
            self.retrieve_tasks()
            self.update_task_list()

    def update_task_list(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        for task in self.tasks:
            task_frame = ttk.Frame(self.task_frame)
            task_frame.grid(row=len(self.task_frame.grid_slaves()) + 1, column=0, columnspan=2, sticky='ew')

            task_label = ttk.Label(task_frame, text=f"{task[1]} - Priority: {task[2]} - Due Date: {task[3]}", width=50,
                                   anchor='w')
            task_label.grid(row=0, column=0, padx=5, pady=5)

            delete_button = ttk.Button(task_frame, text="Delete", command=lambda t=task[0]: self.delete_task(t))
            delete_button.grid(row=0, column=1, padx=5, pady=5)

    def retrieve_tasks(self):
        self.tasks = []
        for row in self.cursor.execute('''SELECT * FROM tasks'''):
            self.tasks.append(row)


def main():
    root = tk.Tk()

    style = ttk.Style()
    style.configure("AddButton.TButton", background="#4CAF50", foreground="orange", font=("Arial", 12))

    task_manager = TaskManager(root)

    root.mainloop()


if __name__ == "__main__":
    main()
