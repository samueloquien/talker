import tkinter as tk
from talker import Talker

talker = Talker()

root = tk.Tk()
root.title("Talker Application")
root.geometry("400x200")
root.resizable(False, False)

label = tk.Label(root, text="Enter text to speak:")
label.pack(pady=10)

entry_box = tk.Entry(root, width=40)
entry_box.pack(pady=5)

def process_entry_text():
    talker.receive_question(entry_box.get())
    entry_box.delete(0, tk.END)

# create a button and attach it to the process_entry_text function
button = tk.Button(root, text="Speak", command=process_entry_text)
button.pack(pady=5)

root.mainloop()
