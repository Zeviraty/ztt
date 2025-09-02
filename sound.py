import numpy as np
import sounddevice as sd
import soundfile as sf

def sine_wave(frequency:int, duration:float, samplerate:int=44100):
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    return np.sin(2 * np.pi * frequency * t)

def square_wave(frequency:int, duration:float, samplerate:int=44100):
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    return np.sign(np.sin(2 * np.pi * frequency * t))

def sawtooth_wave(frequency:int, duration:float, samplerate:int=44100):
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    return 2 * (t * frequency - np.floor(0.5 + t * frequency))

def triangle_wave(frequency:int, duration:float, samplerate:int=44100):
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    return 2 * np.abs(sawtooth_wave(frequency, duration, samplerate)) - 1

def noise_wave(duration:float, samplerate:int=44100):
    return np.random.uniform(-1, 1, int(samplerate * duration))

def play(wave,samplerate=44100):
    wave = wave.astype(np.float32)
    sd.play(wave, samplerate)

def play_wav(location:str):
    data, fs = sf.read(location)
    sd.play(data, fs)

def wait():
    sd.wait()
