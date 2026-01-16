import numpy as np
import pyaudio
import os
import time

# Configuration
FILE_PATH = "image.jpg"  # Path to the file to monitor
BASE_FREQ = 440  # Starting frequency (Hz)
MAX_FREQ = 2000  # Maximum frequency (Hz)
MIN_SIZE = 1024  # Minimum file size in bytes (1 KB)
MAX_SIZE = 100 * 1024  # Maximum file size in bytes (100 KB)
CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
		output_device_index=1,
                frames_per_buffer=CHUNK)

def get_frequency_from_size(file_size):
    """Map file size to frequency between BASE_FREQ and MAX_FREQ."""
    if file_size <= MIN_SIZE:
        return BASE_FREQ
    if file_size >= MAX_SIZE:
        return MAX_FREQ
    # Linear interpolation
    ratio = (file_size - MIN_SIZE) / (MAX_SIZE - MIN_SIZE)
    return BASE_FREQ + ratio * (MAX_FREQ - BASE_FREQ)

def generate_tone(freq, duration=0.1):
    """Generate a sine wave tone for given frequency and duration."""
    samples = np.sin(2 * np.pi * freq * np.arange(RATE * duration) / RATE)
    return samples.astype(np.float32).tobytes()

# Main loop
print(f"Monitoring file: {FILE_PATH} (Ctrl+C to stop)")
try:
    while True:
        if os.path.exists(FILE_PATH):
            file_size = os.path.getsize(FILE_PATH)
            freq = get_frequency_from_size(file_size)
            print(f"File size: {file_size} bytes → Frequency: {freq:.1f} Hz")
            stream.write(generate_tone(freq))
        else:
            print("File not found. Waiting...")
        time.sleep(0.5)  # Check every 0.5 seconds

except KeyboardInterrupt:
    print("\nStopping...")
    stream.stop_stream()
    stream.close()
    p.terminate()   
