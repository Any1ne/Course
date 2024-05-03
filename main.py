import tkinter as tk
from tkinter import ttk, messagebox
import animation
import gui

def run_gui():
    # Створення головного вікна
    root = tk.Tk()
    root.title("Метод Ньютона")

    # Створення екземпляра GUI
    gui_instance = gui.GUI(root)

    # Запуск створення GUI
    gui_instance.create_gui()

    # Запуск циклу обробки подій
    root.mainloop()

if __name__ == "__main__":
    run_gui()

