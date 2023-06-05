# buffers.py
import os, sys
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

os.environ['OPENAI_API_KEY'] = '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'

class AI():
    def __init__(self, instructions:str=None, verbose:bool=True):
        self.instructions : str = instructions
        self.verbose : bool = verbose
        if instructions is None:
            self.instructions = '''You are a friendly and funny version of Frida Kahlo (the Mexican painter). You provide short but funny answers. You are interested in knowing more about the person you're talking to.'''
        self.history = [SystemMessage(content=self.instructions)]
        self.chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    def reset(self, instructions:str=None):
        if instructions is not None:
            self.instructions = instructions
        self.history = [SystemMessage(content=self.instructions)]
        
    def ask(self, question:str):
        self.history.append(HumanMessage(content=question))
        if self.verbose:
            print("Human: " + question)
        result = self.chat(self.history)
        self.history.append(result)
        if self.verbose:
            print("AI:    " + result.content)
        return result.content
    
if __name__ == '__main__':
    ai = AI()
    print(ai.ask('Hello!'))
    