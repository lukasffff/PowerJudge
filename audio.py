import numpy as np
import sounddevice as sd

def play_audio(frequency=880, duration=0.2):

    sample_rate = 44100

    t = np.linspace(0, duration, int(sample_rate * duration), False)

    wave = 0.5 * np.sin(2 * np.pi * frequency * t)

    sd.play(wave, sample_rate)