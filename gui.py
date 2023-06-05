import tkinter as tk

class GUI:
    def __init__(self, talker):
        self.talker = talker

        self.window = tk.Tk()
        self.window.title('Talker')
        self.window.geometry("400x200")
        self.window.resizable(False, False)

        self.label = tk.Label(self.window, text='Talk to me!')
        self.label.pack()

        self.entry = tk.Entry(self.window)
        self.entry.pack()

        self.button = tk.Button(self.window, text='Speak', command=self.speak_text)
        self.button.pack()

    def speak_text(self):
        self.talker.receive_question(self.entry.get())
        self.entry.delete(0, tk.END)

    def run(self):
        self.window.mainloop()

