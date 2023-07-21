import pyttsx3

voice_language = {
    'ES': 0,
    'EN': 1
}

class T2S:
    def __init__(self, language='ES'):
        self.engine =  pyttsx3.init()
        self.set_language(language)
    
    def set_language(self, language:str):
        voices = self.engine.getProperty('voices')
        try:
            voice_index = voice_language[language]
            self.engine.setProperty('voice', voices[voice_index].id)
        except KeyError:
            print('Invalid language '+ language)
            print('Valid values are: ', voice_language.keys())
    
    def speak(self, text:str):
        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == '__main__':
    t2s = T2S('EN')
    t2s.speak('Hello world!')
    t2s.speak('Hola mundo')
    print('Done')

