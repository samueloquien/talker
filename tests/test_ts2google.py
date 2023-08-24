import pytest
from unittest.mock import patch, MagicMock
from google.cloud.texttospeech import SynthesizeSpeechResponse, TextToSpeechClient
from voice_chat_utils import T2SGoogle
from pathlib import Path
import pygame

    
class TestTS2Google:
    
    ts2_init_testdata = [
        ('en', 'male', 'en-US-Standard-A'),
        ('en', 'female', 'en-US-Standard-B'),
        ('es', 'male', 'es-ES-Standard-B'),
        ('es','female','es-ES-Standard-A'),
        ('xx','female',''),
        ('es','nogender',''),
        ('es','',''),
        ('','male',''),
        ('','','')
    ]
    
    save_synthesize_response_to_file_testdata = [
        (MagicMock(SynthesizeSpeechResponse),'test_file.wav', True),
        (MagicMock(SynthesizeSpeechResponse),'test_file.WAV', True),
        (MagicMock(SynthesizeSpeechResponse),'test_file.mp3', False),
        (MagicMock(SynthesizeSpeechResponse),'test_file.txt', False),
        (MagicMock(SynthesizeSpeechResponse),'test_file', False),
        (MagicMock(SynthesizeSpeechResponse),'', False),
        (None,'test_file.wav', False),
        (b'binary content','test_file.wav', False)
    ]
    
    speak_testdata = [
        (True,True,1),
        (False,True,0),
        (True,False,0)
    ]
    
    @pytest.fixture
    def client(self):
        with patch.object(TextToSpeechClient, 'from_service_account_file') as mocked_client:
            yield mocked_client

    @pytest.fixture
    def pygame_sound(self):
        with patch.object(pygame.mixer, 'Sound') as mocked_sound:
            yield mocked_sound

    @pytest.fixture
    def clean(self):
        files_to_delete = ['test_file.wav']
        yield
        for f in files_to_delete:
            p = Path(f)
            p.unlink(missing_ok=True)
            
    @pytest.mark.parametrize("lang,gender,voice", ts2_init_testdata)
    def test_t2s_init(self, lang, gender, voice, client):
        t2s = T2SGoogle(language=lang, gender=gender)
        if t2s.client is not None:
            client.assert_called_once()
        assert t2s.voice == voice
        if not t2s.voice:
            assert t2s.client is None

    def test_get_unique_languages_from_voices(self, client):
        voices = [MagicMock(language_codes=['en-US', 'es-ES']), MagicMock(language_codes=['en-GB'])]
        t2s = T2SGoogle()
        result = t2s.get_unique_languages_from_voices(voices)
        assert result == set(['en-US', 'es-ES', 'en-GB'])

    def test_list_languages(self, client):
        voices = [MagicMock(language_codes=['en-US', 'es-ES']), MagicMock(language_codes=['en-GB'])]
        client.return_value.list_voices.return_value.voices = voices
        t2s = T2SGoogle()
        languages = t2s.list_languages()
        client.return_value.list_voices.assert_called_once()
        assert languages == set(['en-US', 'es-ES', 'en-GB'])

    def test_list_voices(self, client):
        voices_mock = [MagicMock(name='en-US-Wavenet-F', language_codes=['en-US'], ssml_gender=1, natural_sample_rate_hertz=24000)]
        voices_mock[0].name = 'en-US-Wavenet-F' # to mock the 'name' attribute, you must do it after instantiating the MagicMock object
        client.return_value.list_voices.return_value.voices = voices_mock
        t2s = T2SGoogle()
        voices = t2s.list_voices()
        client.return_value.list_voices.assert_called_once()
        voices_names = [v.name for v in voices]
        voices_mock_names = [v.name for v in voices_mock]
        assert voices_names == voices_mock_names

    @pytest.mark.parametrize("response,filename,expected_success", save_synthesize_response_to_file_testdata)
    def test_save_synthesize_response_to_file(self, response, filename, expected_success, client, clean):
        if isinstance(response, SynthesizeSpeechResponse):
            response.audio_content = b"dummy audio content"
        t2s = T2SGoogle()
        assert t2s.save_synthesize_response_to_file(response, filename) == expected_success
        path = Path(filename)
        if expected_success:
            assert path.is_file()
            assert path.stat().st_size > 0
        else:
            assert path.is_file() == False

    @pytest.mark.parametrize("hasVoice,hasClient,expected_num_reproductions", speak_testdata)
    def test_speak(self, hasVoice,hasClient,expected_num_reproductions, client, pygame_sound):
        t2s = T2SGoogle()
        if hasClient:
            client.return_value.synthesize_speech.return_value.audio_content = b"dummy audio content"
        else:
            t2s.client = None
        if not hasVoice:
            t2s.voice = ''
        t2s.speak('Hello, World!')
        if hasVoice and hasClient:
            client.return_value.synthesize_speech.assert_called_once()
        assert pygame_sound.return_value.play.call_count == expected_num_reproductions
