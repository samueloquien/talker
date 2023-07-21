from t2s import T2S
from t2s_google import T2SGoogle
from voice_chat_utils.ai import AI
from gui import GUI

class Talker:
    def __init__(self):
        self.t2s = T2SGoogle('es','female')
        self.ai = AI(verbose=True)
        
    def receive_question(self, question:str):
        answer = self.ai.ask(question)
        self.t2s.speak(answer)

if __name__ == '__main__':
    talker = Talker()
    gui = GUI(talker)
    gui.run()