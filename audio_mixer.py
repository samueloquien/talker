import pyaudio
import wave

class AudioMixer:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
    
    def record(self, max_seconds:int=5, output_filename='output.wav'):

        # Set audio parameters
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = max_seconds
        WAVE_OUTPUT_FILENAME = output_filename

        # Initialize audio stream
        stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        # Record audio
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        # Stop recording
        stream.stop_stream()
        stream.close()
        self.audio.terminate()
        self.recorded_audio_content = b''.join(frames)

        # Save audio to file
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(self.recorded_audio_content)
        waveFile.close()

if __name__ == '__main__':
    m = AudioMixer()
    print('Recording...')
    m.record()
    print('done.')
        