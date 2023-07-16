from google.cloud import speech

class STTGoogle:
    def __init__(self, language:str='en'):
        self.client : speech.SpeechClient = speech.SpeechClient.from_service_account_file('talker-388916-fcf495d2e4a2.json')
        self.language : str = language
        self.recognized_text : str = ''

        # RecognitionConfig for WAV files
        self.config_file = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="es",
        )

        # RecognitionConfig for AudioMixer audio
        self.config_audio_mixer = speech.RecognitionConfig(
            encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz = 44100,
            audio_channel_count = 1,
            language_code = 'es',
            enable_automatic_punctuation=True,
            enable_spoken_punctuation=False
        )

    # Synchronous speech recognition request
    def __recognize_audio(self, config: speech.RecognitionConfig, audio: speech.RecognitionAudio):
        self.recognized_response = self.client.recognize(config=config, audio=audio)
        self.recognized_response.results[0].language_code
        self.recognized_text = self.recognized_response.results[0].alternatives[0].transcript
    
    def __print_response_parameters(self):
        result = self.recognized_response.results[0]
        language_code = result.language_code
        best_alternative = result.alternatives[0]
        print("-" * 80)
        print(f"language_code: {language_code}")
        print(f"transcript:    {best_alternative.transcript}")
        print(f"confidence:    {best_alternative.confidence:.0%}")

    def transcribe_file(self, filename:str):
        with open(filename,'rb') as f:
            audio_content = f.read()
        audio = speech.RecognitionAudio(content=audio_content)
        self.__recognize_audio(self.config_file, audio)
        return self.recognized_text

    '''
    Invoke Google's speech recognition using a configuration compatible
    with AudioMixer's output
    '''
    def transcribe_audio(self, audio_content):
        audio = speech.RecognitionAudio(content=audio_content)
        self.__recognize_audio(self.config_audio_mixer, audio)
        return self.recognized_text

    

