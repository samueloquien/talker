import pytest
from unittest.mock import patch, MagicMock
from voice_chat_utils import S2TGoogle
from google.cloud.speech import SpeechClient


class TestS2TGoogle:

    transcribe_file_testdata = [
        ("tests/resources/quesuenotengo.wav","Hello World!"),
        ("nonexisting_file","")
    ]
    
    @pytest.fixture
    def client(self):
        with patch.object(SpeechClient, 'from_service_account_file') as mocked_client:
            yield mocked_client

    @pytest.mark.parametrize('filename,expected_result', transcribe_file_testdata)
    def test_transcribe_file_with_mocked_client(self, filename, expected_result, client):
        recognized_response = MagicMock(results=[MagicMock(alternatives=[MagicMock(transcript='Hello World!')])])
        client.return_value.recognize.return_value = recognized_response
        s2t = S2TGoogle('es')
        result = s2t.transcribe_file(filename)
        assert result == expected_result

    def test_transcribe_file_with_real_client(self):
        filename = 'tests/resources/quesuenotengo.wav'
        expected_result = 'qué sueño tengo'
        s2t = S2TGoogle('es')
        result = s2t.transcribe_file(filename)
        assert result == expected_result

    def test_transcribe_audio(self, client):
        recognized_response = MagicMock(results=[MagicMock(alternatives=[MagicMock(transcript='Hello World!')])])
        client.return_value.recognize.return_value = recognized_response
        s2t = S2TGoogle('es')
        result = s2t.transcribe_audio(b"mock_audio_content")
        assert result == "Hello World!"
