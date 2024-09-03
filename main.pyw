import tkinter as tk, random, win32com.client, subprocess, ctypes, appdirs
from tkinter import ttk, filedialog

window = tk.Tk()
window.title("Files & Folders on Taskbar")
window.resizable(False, False)
window.configure(padx = 14, pady = 8)

working_folder = appdirs.user_data_dir("Files & Folders on Taskbar", False) + "\\Shortcut"
shortcut_type = tk.StringVar(value = "file")
use_folder_icon = tk.BooleanVar(value = False)

def pick_icon(default_icon = "C:\\Windows\\System32\\shell32.dll,0") -> str:
    icon_file_buffer = ctypes.create_unicode_buffer(260)
    icon_index = ctypes.c_int(0)

    initial_icon_file = "C:\\Windows\\System32\\shell32.dll"
    ctypes.windll.kernel32.lstrcpyW(icon_file_buffer, initial_icon_file)

    result = ctypes.windll.shell32.PickIconDlg(None, icon_file_buffer, ctypes.sizeof(icon_file_buffer), ctypes.byref(icon_index))

    if result: return f"{icon_file_buffer.value},{icon_index.value}"
    else: return default_icon

def open_working_folder():
    subprocess.call(f"explorer \"{working_folder}\"", shell = True)

def browse():
    subprocess.call(f"rmdir /q /s \"{working_folder}\"", shell = True)
    subprocess.call(f"mkdir \"{working_folder}\"", shell = True)

    if shortcut_type.get() == "file":
        file = filedialog.askopenfile(title = "Choose a file", parent = window)

        if not file.name == "": create_file_shortcut(file.name); open_working_folder()
        else: return
    else:
        folder = filedialog.askdirectory(title = "Choose a folder", parent = window).replace("\"", "")

        if not folder == "": create_folder_shortcut(folder); open_working_folder()
        else: return

    ctypes.windll.user32.MessageBoxW(
        0,
        "The shortcut has been created.\n\nNow, a File Explorer window with the folder where was the shortcut created was opened. Drag the shortcut to your taskbar and then close the File Explorer window.\n\nYou have to do this extra step, because it's not that easy for 3rd party programs to pin a shortcut in the taskbar on Windows 10 and 11.", 
        "Files & Folders on Taskbar", 
        0x40 | 0x40000
    )

def create_file_shortcut(file_path):
    path_list = file_path.split("/")
    file_name = path_list[len(path_list) - 1]
    random_number = str(random.randint(1000, 9999))

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(f"{working_folder}\\{file_name}.lnk")
    shortcut.TargetPath = "C:\\Windows\\explorer.exe"
    shortcut.WorkingDirectory = (file_path + random_number).replace(file_name + random_number, "")
    shortcut.Arguments = f"\"{file_name}\""
    shortcut.IconLocation = pick_icon()
    shortcut.save()

def create_folder_shortcut(folder_path):
    folder_icon = "C:\\Windows\\System32\\shell32.dll,4"  # Default folder icon
    folder_config = subprocess.getoutput(f"type \"{folder_path}\\desktop.ini\"").split("\n")

    if use_folder_icon.get():
        for line in folder_config:
            if line.startswith("IconResource="):
                folder_icon = line.replace("IconResource=", "")
    else: folder_icon = pick_icon("C:\\Windows\\System32\\shell32.dll,4")

    path_list = folder_path.split("/")
    folder_name = path_list[len(path_list) - 1]
    random_number = str(random.randint(1000, 9999))

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(f"{working_folder}\\{folder_name}.lnk")
    shortcut.TargetPath = "C:\\Windows\\explorer.exe"
    shortcut.WorkingDirectory = (folder_path + random_number).replace(folder_name + random_number, "")
    shortcut.Arguments = f"\"{folder_name}\""
    shortcut.IconLocation = folder_icon
    shortcut.save()

def file_selected():
    pin_it_btn["text"] = "Choose a file & pin it to taskbar"
    use_folder_icon_tick.forget()

def folder_selected():
    pin_it_btn["text"] = "Choose a folder & pin it to taskbar"
    use_folder_icon_tick.pack(fill = "x", pady = (8, 0))
    pin_it_btn.forget()
    pin_it_btn.pack(fill = "x", pady = (16, 4))

ttk.Label(window, text = "Files & Folders on Taskbar", font = ("Segoe UI Semibold", 17)).pack(anchor = "w")

ttk.Label(window, text = "Pin to taskbar a shortcut to:").pack(anchor = "w", pady = 8)
ttk.Radiobutton(window, text = "A file", variable = shortcut_type, value = "file", command = file_selected).pack(anchor = "w")
ttk.Radiobutton(window, text = "A folder", variable = shortcut_type, value = "folder", command = folder_selected).pack(anchor = "w")

use_folder_icon_tick = ttk.Checkbutton(window, text = "Use folder's icon", variable = use_folder_icon)

pin_it_btn = ttk.Button(window, text = "Choose a file & pin it to taskbar", default = "active", command = browse)
pin_it_btn.pack(fill = "x", pady = (16, 4))

window.mainloop()