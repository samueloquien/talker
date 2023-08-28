from typing import Any
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
load_dotenv()

class AI():
    """
    An AI class that interfaces with OpenAI's GPT for answering questions.
    """

    def __init__(self, instructions: str = '', verbose: bool = False) -> None:
        """
        Initializes the AI class.

        :param instructions: Instructions to set the behavior of the AI. Default is a description of a friendly and funny Frida Kahlo.
        :param verbose: Whether to print interactions to the console. Default is False.
        """
        self.instructions: str = instructions
        self.verbose: bool = verbose
        if not instructions:
            self.instructions = '''You are a friendly and funny version of Frida Kahlo (the Mexican painter). You provide short but funny answers. You are interested in knowing more about the person you're talking to.'''
        # Initialize history with the instruction message
        self.history: list[Any] = [SystemMessage(content=self.instructions)]
        # Initialize the chat model
        self.chat = ChatOpenAI(client=None, model="gpt-3.5-turbo", temperature=0)

    def reset(self, instructions: str = '') -> None:
        """
        Resets the chat history and optionally updates the instructions.

        :param instructions: New instructions to set the behavior of the AI. If not provided, the original instructions are used.
        """
        if instructions:
            self.instructions = instructions
        self.history = [SystemMessage(content=self.instructions)]
        
    def ask(self, question: str) -> str:
        """
        Asks the AI a question and gets a response.

        :param question: The question to ask the AI.
        :return: The AI's response as a string.
        """
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
    # Test the AI class
    ai = AI(verbose=True)
    ai.ask('Hello!')
    ai.ask('What is your name?')
