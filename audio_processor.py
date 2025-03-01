import numpy as np
import sounddevice as sd
import librosa
import wave
from scipy.signal import butter, lfilter
from typing import List, Tuple
import threading
import queue
import time

class MorseAudioProcessor:
    def __init__(self):
        self.SAMPLE_RATE = 44100
        self.CHUNK_SIZE = 1024
        self.THRESHOLD = 0.1  # Signal amplitude threshold
        self.DOT_DURATION = 0.1  # seconds
        self.DASH_DURATION = 0.3  # seconds
        self.SILENCE_DURATION = 0.1  # seconds
        self.audio_queue = queue.Queue()
        self.is_recording = False

    def butter_bandpass(self, lowcut: float, highcut: float, order: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """Create a butterworth bandpass filter."""
        nyquist = 0.5 * self.SAMPLE_RATE
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def bandpass_filter(self, data: np.ndarray, lowcut: float = 500, highcut: float = 1500) -> np.ndarray:
        """Apply bandpass filter to the audio data."""
        b, a = self.butter_bandpass(lowcut, highcut)
        return lfilter(b, a, data)

    def detect_morse_signals(self, audio_data: np.ndarray) -> List[Tuple[str, float]]:
        """Detect Morse code signals in audio data."""
        # Normalize audio
        audio_data = audio_data / np.max(np.abs(audio_data))
        
        # Apply bandpass filter
        filtered_data = self.bandpass_filter(audio_data)
        
        # Calculate signal envelope
        envelope = np.abs(filtered_data)
        
        # Detect signals above threshold
        signals = []
        is_signal = False
        start_time = 0
        
        for i in range(len(envelope)):
            time_point = i / self.SAMPLE_RATE
            
            if envelope[i] > self.THRESHOLD and not is_signal:
                is_signal = True
                start_time = time_point
            elif envelope[i] <= self.THRESHOLD and is_signal:
                is_signal = False
                duration = time_point - start_time
                
                if duration >= self.DASH_DURATION:
                    signals.append(('-', start_time))
                elif duration >= self.DOT_DURATION:
                    signals.append(('.', start_time))
                    
        return signals

    def process_audio_file(self, file_path: str) -> str:
        """Process audio file and return Morse code."""
        if file_path.endswith('.mp3'):
            # Load MP3 using librosa
            audio_data, _ = librosa.load(file_path, sr=self.SAMPLE_RATE)
        else:
            # Load WAV file
            with wave.open(file_path, 'rb') as wav_file:
                audio_data = np.frombuffer(wav_file.readframes(-1), dtype=np.int16)
                audio_data = audio_data.astype(np.float32) / 32768.0  # Normalize

        signals = self.detect_morse_signals(audio_data)
        return ' '.join([signal[0] for signal in signals])

    def audio_callback(self, indata: np.ndarray, frames: int, time_info: dict, status: int) -> None:
        """Callback for processing live audio input."""
        if status:
            print(f'Audio callback error: {status}')
        if self.is_recording:
            self.audio_queue.put(indata.copy())

    def start_live_recording(self) -> None:
        """Start recording from audio input."""
        self.is_recording = True
        self.audio_queue = queue.Queue()
        
        # Start audio stream
        stream = sd.InputStream(
            channels=1,
            samplerate=self.SAMPLE_RATE,
            blocksize=self.CHUNK_SIZE,
            callback=self.audio_callback
        )
        stream.start()
        return stream

    def stop_live_recording(self, stream: sd.InputStream) -> str:
        """Stop recording and process the recorded audio."""
        self.is_recording = False
        stream.stop()
        stream.close()
        
        # Collect all audio data from queue
        audio_chunks = []
        while not self.audio_queue.empty():
            audio_chunks.append(self.audio_queue.get())
        
        if not audio_chunks:
            return ""
            
        # Combine chunks and process
        audio_data = np.concatenate(audio_chunks)
        signals = self.detect_morse_signals(audio_data.flatten())
        return ' '.join([signal[0] for signal in signals])
