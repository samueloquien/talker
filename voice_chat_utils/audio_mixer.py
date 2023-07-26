import pyaudio
import wave

class AudioMixer:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.recorded_audio_content = None
        # Set audio parameters
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
    
    def record(self, max_seconds:int=5):

        # Initialize audio stream
        stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        # Record audio
        frames = []
        for i in range(0, int(self.RATE / self.CHUNK * max_seconds)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        # Stop recording
        stream.stop_stream()
        stream.close()
        self.audio.terminate()
        self.recorded_audio_content = b''.join(frames)

    # Save audio to file
    def save_recorded_audio(self, filename:str):
        if filename[-4:].upper() != '.WAV':
            filename += '.wav'
        waveFile = wave.open(filename, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(self.recorded_audio_content)
        waveFile.close()

if __name__ == '__main__':
    m = AudioMixer()
    print('Recording...')
    m.record()
    print('done.')
    m.save_recorded_audio('output.wav')
        