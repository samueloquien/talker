import os
from typing import Any
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

os.environ['OPENAI_API_KEY'] = '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'

class AI():
    def __init__(self, instructions:str='', verbose:bool=False):
        self.instructions : str = instructions
        self.verbose : bool = verbose
        if not instructions:
            self.instructions = '''You are a friendly and funny version of Frida Kahlo (the Mexican painter). You provide short but funny answers. You are interested in knowing more about the person you're talking to.'''
        self.history : list[Any] = [SystemMessage(content=self.instructions)]
        self.chat = ChatOpenAI(client=None, model="gpt-3.5-turbo", temperature=0)
    
    def reset(self, instructions:str=''):
        if instructions:
            self.instructions = instructions
        self.history = [SystemMessage(content=self.instructions)]
        
    def ask(self, question:str):
        self.history.append(HumanMessage(content=question))
        if self.verbose:
            print("Human: " + question)
        try:
            result = self.chat(self.history)
        except:
            result = AIMessage(content="I cannot provide an answer right now. Please, try again later.")
        self.history.append(result)
        if self.verbose:
            print("AI:    " + result.content)
        return result.content
    
if __name__ == '__main__':
    ai = AI(verbose=True)
    ai.ask('Hello!')
    ai.ask('What is your name?')
    