from typing import Sequence
import google.cloud.texttospeech as tts
import io
import pygame

class T2SGoogle:
    """
    A Python class to convert text to speech using Google Cloud Text To Speech service.
    """

    def __init__(self, language: str = 'en', gender: str = 'male'):
        """
        Initialize the T2SGoogle class with language and gender parameters.

        :param language: Language code for the text. Default is 'en'.
        :param gender: Voice gender. Can be 'male' or 'female'. Default is 'male'.
        """
        preferred_voices = {
            "en": {'male': 'en-US-Standard-A', 'female': 'en-US-Standard-B'},
            "es": {'male': 'es-ES-Standard-B', 'female': 'es-ES-Standard-A'}
        }
        try:
            self.voice: str = preferred_voices[language][gender]
            self.client: tts.TextToSpeechClient | None = tts.TextToSpeechClient.from_service_account_file('talker_google_service_account_settings.json')
        except:
            self.voice = ''
            self.client = None
        pygame.init()

    def get_unique_languages_from_voices(self, voices: Sequence[tts.Voice]):
        """
        Extracts unique languages from a sequence of Voice objects.

        :param voices: Sequence of Google TextToSpeech Voice objects.
        :return: Set of unique language codes.
        """
        language_set = set()
        for voice in voices:
            for language_code in voice.language_codes:
                language_set.add(language_code)
        return language_set

    def list_languages(self):
        """
        Lists and prints the available languages.

        :return: Set of available languages.
        """
        response = self.client.list_voices()
        languages = self.get_unique_languages_from_voices(response.voices)

        print(f" Languages: {len(languages)} ".center(60, "-"))
        for i, language in enumerate(sorted(languages)):
            print(f"{language:>10}", end="\n" if i % 5 == 4 else "")

        return languages

    def list_voices(self, language_code=None):
        """
        Lists and prints the available voices for a specific language.

        :param language_code: Optional parameter to filter voices by language.
        :return: List of available voices.
        """
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

    def save_synthesize_response_to_file(self, response: tts.SynthesizeSpeechResponse, filename: str):
        """
        Saves the synthesized speech response to a .wav file.

        :param response: Google Cloud TextToSpeech SynthesizeSpeechResponse object.
        :param filename: Name of the output .wav file.
        :return: Boolean indicating success or failure.
        """
        if not filename[-4:].lower() == '.wav':
            print('Invalid file name extension. Only .wav files are supported.')
            return False
        if not isinstance(response, tts.SynthesizeSpeechResponse):
            print("Invalid parameter 'response'. Must be a SynthesizeSpeechResponse instance.")
            return False
        with open(filename, 'wb') as f:
            f.write(response.audio_content)
        return True

    def speak(self, text: str):
        """
        Converts the input text to speech and plays it.

        :param text: Text string to be converted to speech.
        """
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
        while pygame.mixer.get_busy():  # keep the music playing until the file ends
            continue

if __name__ == '__main__':
    t2s = T2SGoogle('es', 'male')
    t2s.speak('¿Qué sueño tengo?')
