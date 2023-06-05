import tkinter as tk
import pyttsx3


root = tk.Tk()
root.title("Talker Application")
root.geometry("400x200")
root.resizable(False, False)

label = tk.Label(root, text="Enter text to speak:")
label.pack(pady=10)

entry_box = tk.Entry(root, width=40)
entry_box.pack(pady=5)

def speak():
    engine = pyttsx3.init()
    engine.say(entry_box.get())
    engine.runAndWait()
    entry_box.delete(0, tk.END)

# create a button and attach it to the speak function
button = tk.Button(root, text="Speak", command=speak)
button.pack(pady=5)

root.mainloop()

'''
button = tk.Button(root, text="Speak", command=speak)
button.pack(pady=10)

root.mainloop()
'''

'''
sabes que yo no puedo salir
porque no tengo camiseta
'''