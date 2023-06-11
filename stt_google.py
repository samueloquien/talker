from google.cloud import speech

class STTGoogle:
    def __init__(self, language:str='en'):
        self.client = speech.SpeechClient.from_service_account_file('talker-388916-fcf495d2e4a2.json')

def speech_to_text(
    config: speech.RecognitionConfig,
    audio: speech.RecognitionAudio,
) -> speech.RecognizeResponse:
    client = speech.SpeechClient.from_service_account_file('talker-388916-fcf495d2e4a2.json')

    # Synchronous speech recognition request
    response = client.recognize(config=config, audio=audio)

    return response


def print_response(response: speech.RecognizeResponse):
    for result in response.results:
        print_result(result)


def print_result(result: speech.SpeechRecognitionResult):
    best_alternative = result.alternatives[0]
    print("-" * 80)
    print(f"language_code: {result.language_code}")
    print(f"transcript:    {best_alternative.transcript}")
    print(f"confidence:    {best_alternative.confidence:.0%}")

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    language_code="es",
)

with open("response.wav",'rb') as f:
    audio_content = f.read()
    
audio = speech.RecognitionAudio(content=audio_content)

response = speech_to_text(config, audio)
print_response(response)
