from google.cloud import speech

class S2TGoogle:
    """
    A Python class that interfaces with Google Cloud's Speech-to-Text API
    to transcribe audio into text.
    """

    def __init__(self, language:str='en'):
        """
        Initializes the S2TGoogle class.

        :param language: The language of the audio. Default is 'en' (English).
        """
        self.client: speech.SpeechClient = speech.SpeechClient.from_service_account_file('talker_google_service_account_settings.json')
        self.language: str = language
        self.recognized_text: str = ''

        # Configuration settings for WAV audio files
        self.config_file = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="es",
        )

        # Configuration settings specific to AudioMixer audio outputs
        self.config_audio_mixer = speech.RecognitionConfig(
            encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz = 44100,
            audio_channel_count = 1,
            language_code = 'es',
            enable_automatic_punctuation=True,
            enable_spoken_punctuation=False
        )

    def __recognize_audio(self, config: speech.RecognitionConfig, audio: speech.RecognitionAudio):
        """
        A private method to invoke Google's speech recognition.

        :param config: Configuration settings for the speech recognition.
        :param audio: Audio data to transcribe.
        """
        try:
            self.recognized_response = self.client.recognize(config=config, audio=audio)
            if not self.recognized_response.results:
                raise ValueError("No results returned from Google Cloud Speech-to-Text.")
            self.recognized_text = self.recognized_response.results[0].alternatives[0].transcript
        except Exception as e:
            print(f"Error recognizing audio: {e}")
            self.recognized_text = ''

    def __print_response_parameters(self):
        """
        A private method to print the recognized results.
        """
        result = self.recognized_response.results[0]
        language_code = result.language_code
        best_alternative = result.alternatives[0]
        print("-" * 80)
        print(f"language_code: {language_code}")
        print(f"transcript:    {best_alternative.transcript}")
        print(f"confidence:    {best_alternative.confidence:.0%}")

    def transcribe_file(self, filename:str) -> str:
        """
        Transcribes a given audio file.

        :param filename: The path to the audio file.
        :return: The transcribed text.
        """
        try:
            with open(filename, 'rb') as f:
                audio_content = f.read()
            audio = speech.RecognitionAudio(content=audio_content)
            self.__recognize_audio(self.config_file, audio)
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
            self.recognized_text = ''
        return self.recognized_text

    def transcribe_audio(self, audio_content) -> str:
        """
        Transcribes given audio content using a configuration compatible with AudioMixer's output.

        :param audio_content: The audio content to transcribe.
        :return: The transcribed text.
        """
        if not audio_content:
            print("Error: No audio content provided.")
            return ''
        audio = speech.RecognitionAudio(content=audio_content)
        self.__recognize_audio(self.config_audio_mixer, audio)
        return self.recognized_text
