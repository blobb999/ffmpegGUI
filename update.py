#update.py:

import os
import subprocess
import tkinter.messagebox

def update_program():
    try:
        result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
        if 'Already up to date.' in result.stdout:
            tkinter.messagebox.showinfo("Update", "The program is already up to date.")
        else:
            tkinter.messagebox.showinfo("Update", "The program has been updated. Please restart the application.")
            os._exit(0)
    except Exception as e:
        tkinter.messagebox.showerror("Update Error", f"An error occurred while updating the program: {e}")

def update_youtubedl():
    try:
        result = subprocess.run(['pip', 'install', '--upgrade', 'youtube-dl'], capture_output=True, text=True)
        if 'Requirement already up-to-date' in result.stdout:
            tkinter.messagebox.showinfo("Update", "youtube-dl is already up to date.")
        else:
            tkinter.messagebox.showinfo("Update", "youtube-dl has been updated.")
    except Exception as e:
        tkinter.messagebox.showerror("Update Error", f"An error occurred while updating youtube-dl: {e}")
