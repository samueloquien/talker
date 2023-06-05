from t2s import T2S
from ai import AI
from gui import GUI

class Talker:
    def __init__(self):
        self.t2s = T2S()
        self.ai = AI()
        
    def receive_question(self, question:str):
        answer = self.ai.ask(question)
        self.t2s.speak(answer)

if __name__ == '__main__':
    talker = Talker()
    gui = GUI(talker)
    gui.run()