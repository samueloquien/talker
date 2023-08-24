from typing import Sequence
import google.cloud.texttospeech as tts
import io
import pygame

class T2SGoogle:
    def __init__(self, language:str='en', gender:str='male'):
        preferred_voices = {
            "en": {'male':'en-US-Standard-A', 'female':'en-US-Standard-B'},
            "es": {'male':'es-ES-Standard-B', 'female':'es-ES-Standard-A'}
        }
        try:
            self.voice : str = preferred_voices[language][gender]
            self.client : tts.TextToSpeechClient | None = tts.TextToSpeechClient.from_service_account_file('talker-388916-fcf495d2e4a2.json')
        except:
            self.voice = ''
            self.client = None
        pygame.init()

    def get_unique_languages_from_voices(self, voices: Sequence[tts.Voice]):
        language_set = set()
        for voice in voices:
            for language_code in voice.language_codes:
                language_set.add(language_code)
        return language_set


    def list_languages(self):
        response = self.client.list_voices()
        languages = self.get_unique_languages_from_voices(response.voices)

        print(f" Languages: {len(languages)} ".center(60, "-"))
        for i, language in enumerate(sorted(languages)):
            print(f"{language:>10}", end="\n" if i % 5 == 4 else "")
            
        return languages

    def list_voices(self, language_code=None):
        response = self.client.list_voices(language_code=language_code)
        voices = sorted(response.voices, key=lambda voice: voice.name)

        print(f" Voices: {len(voices)} ".center(60, "-"))
        for voice in voices:
            languages = ", ".join(voice.language_codes)
            name = voice.name
            gender = tts.SsmlVoiceGender(voice.ssml_gender).name
            rate = voice.natural_sample_rate_hertz
            print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")
            
        return voices
            
    def save_synthesize_response_to_file(self, response:tts.SynthesizeSpeechResponse, filename:str):
        if not filename[-4:].lower() == '.wav':
            print('Invalid file name extension. Only .wav files are supported.')
            return False
        if not isinstance(response, tts.SynthesizeSpeechResponse):
            print("Invalid parameter 'response'. Must be a SynthesizeSpeechResponse instance.")
            return False
        with open(filename,'wb') as f:
            f.write(response.audio_content)
        return True

    def speak(self, text:str):
        if not text or not self.voice or self.client is None:
            return
        voice_name = self.voice
        language_code = voice_name[:5]
        text_input = tts.SynthesisInput(text=text)
        voice_params = tts.VoiceSelectionParams(
            language_code=language_code, name=voice_name
        )
        audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
        
        response = self.client.synthesize_speech(
            input=text_input,
            voice=voice_params,
            audio_config=audio_config,
        )
        
        self.save_synthesize_response_to_file(response, 'response.wav')
        
        # Play the sound
        sound_file = io.BytesIO(response.audio_content)
        sound = pygame.mixer.Sound(sound_file)
        sound.play()
        print('Ready to speak')
        while pygame.mixer.get_busy(): # keep the music playing until the file ends
            continue

if __name__ == '__main__':
    t2s = T2SGoogle('es','male')
    t2s.speak('¿Qué sueño tengo?')
