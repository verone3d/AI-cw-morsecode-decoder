import pytest
import numpy as np
from audio_processor import MorseAudioProcessor

def test_bandpass_filter():
    processor = MorseAudioProcessor()
    # Create a test signal
    t = np.linspace(0, 1, processor.SAMPLE_RATE)
    test_signal = np.sin(2 * np.pi * 1000 * t)  # 1kHz signal
    
    filtered_signal = processor.bandpass_filter(test_signal)
    assert len(filtered_signal) == len(test_signal)
    assert isinstance(filtered_signal, np.ndarray)

def test_detect_morse_signals():
    processor = MorseAudioProcessor()
    # Create a test signal with a dot and dash
    duration = 1  # second
    t = np.linspace(0, duration, int(duration * processor.SAMPLE_RATE))
    
    # Create a dot (0.1s) and a dash (0.3s)
    signal = np.zeros_like(t)
    dot_samples = int(0.1 * processor.SAMPLE_RATE)
    dash_samples = int(0.3 * processor.SAMPLE_RATE)
    
    # Add dot
    signal[:dot_samples] = np.sin(2 * np.pi * 1000 * t[:dot_samples])
    # Add dash
    signal[-dash_samples:] = np.sin(2 * np.pi * 1000 * t[:dash_samples])
    
    signals = processor.detect_morse_signals(signal)
    assert len(signals) == 2
    assert signals[0][0] == '.'  # First signal should be a dot
    assert signals[1][0] == '-'  # Second signal should be a dash
