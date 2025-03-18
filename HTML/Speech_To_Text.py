
#!pip install -r requirements.txt
import soundfile as sf
import pyaudio
import wave
from openai import OpenAI
import whisper
import torch

import subprocess
import sys

# Install the package if not already installed
try:
    import ffmpeg
except ImportError:
    print("Installing ffmpeg-python...")
    subprocess.run([sys.executable, "-m", "pip", "install", "ffmpeg-python"], check=True)
    import ffmpeg


# In[3]:


def record_audio(): #Function to record audio
       
    FORMAT = pyaudio.paInt16 # data format
    CHANNELS = 1 # mono, change to 2 if you want stereo
    RATE = 44100 # sample rate
    CHUNK = 1024 # frames per buffer
    RECORD_SECONDS = 25 # change this to the duration you want to record
    WAVE_OUTPUT_FILENAME = "output.wav"

    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

import os
import subprocess
import whisper

def convert_video_to_text(video_file):
    """
    Extracts audio from a video file using ffmpeg and converts it to text using the locally downloaded Whisper model.
    """

    # Check if video file exists
    if not os.path.isfile(video_file):
        raise FileNotFoundError(f"Error: The file '{video_file}' was not found.")

    # Define temporary audio output file
    audio_path = "temp_audio.wav"

    try:
        # Extract audio using ffmpeg
        command = [
            "ffmpeg", "-i", video_file, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path, "-y"
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Load Whisper model
        model = whisper.load_model("large")

        # Transcribe the extracted audio
        result = model.transcribe(audio_path)

        # Cleanup: Remove temporary audio file
        os.remove(audio_path)

        return result["text"]  # Extract and return transcribed text

    except Exception as e:
        print(f"Error processing video: {e}")
        return None


# In[5]:




# In[6]:


import ffmpeg

def convert_mp3_to_wav(input_mp3, output_wav):
    """Converts an MP3 file to WAV format using FFmpeg."""
    try:
        ffmpeg.input(input_mp3).output(output_wav, ar=16000, ac=1, format='wav').run(overwrite_output=True)
        print(f"Conversion successful: {output_wav}")
    except Exception as e:
        print(f"Error during conversion: {e}")


# In[10]:


def main():
   # record_audio()
    audio_path = "output.wav" 
    convert_mp3_to_wav(audio_path, "output.wav")
    transcribed_text = convert_audio_to_text("output.wav")
    print(transcribed_text)


# In[ ]:


#main()


# In[16]:


import pyaudio
import wave
import threading

# Audio settings
FORMAT = pyaudio.paInt16  # 16-bit audio
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate (Hz)
CHUNK = 1024  # Frames per buffer
WAVE_OUTPUT_FILENAME = "recorded_audio.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()
stream = None
frames = []
recording = False

def start_recording():
    """Start recording audio."""
    global stream, frames, recording
    if recording:
        print("Recording is already in progress...")
        return

    recording = True
    frames = []  # Clear previous recording

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("🎙️ Recording started...")
    
    def record():
        while recording:
            data = stream.read(CHUNK)
            frames.append(data)

    # Start recording in a separate thread
    threading.Thread(target=record, daemon=True).start()

def stop_recording():
    """Stop recording and save the audio file."""
    global stream, frames, recording
    if not recording:
        print("No recording is in progress.")
        return

    recording = False  # Stop recording loop
    stream.stop_stream()
    stream.close()

    # Save the recording to a WAV file
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"✅ Recording stopped and saved as {WAVE_OUTPUT_FILENAME}")


get_ipython().system('jupyter nbconvert --to script Speech_To_Text.ipynb')

