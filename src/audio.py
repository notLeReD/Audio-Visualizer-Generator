#TODO:
# - lookup different audio systems/handlers for python
# - possible choices: (https://wiki.python.org/python/multimedia/Audio.html)
#   - pyAudio: bindings for PortAudio input/output
#   - pyDub: audio manipulation
#   - ffmpeg: decoder, encoder, transcoder, mux, streamer


import os
import subprocess
import tempfile
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play
from pydub.playback import _play_with_ffplay

#change these later when implementing
DIR_AUDIO = Path(__file__).resolve().parent.parent/"audio"
extensions = [".mp3", ".wav", ".aif", ".flac", ".alac", ".wma", ".aac", ".ogg"]
patterns = " ".join(f"*{ext}" for ext in extensions)
FILETYPES = [
    ("Audio files", patterns),
    ("MP3", "*.mp3"),
    ("WAV", "*.wav"),
    ("FLAC", "*.flac"),
    ("All files", "*.*"),
]

class Song():

    def __init__(self, audio):
        self.song = audio
        self.channels = audio.channels
        self.frame_rate = audio.frame_rate
        self.sample_width = audio.sample_width
        self.dBFS = audio.dBFS
        self.peak_amp = audio.max

    def __str__(self):
        return f"{self.channels}, {self.frame_rate}, {self.sample_width}, {self.dBFS}, {self.peak_amp}, {len(self.song)}"

    """
    A custom ffplay wrapper to play audio files

    - PyDub has a common Windows bug with it's built in ffplay player 
    where tempfiles cannot be played due to a PermissionDenied error

    - To avoid this:
    1. Create temp file (mkstemp)
    2. Close Python's handle on it
    3. Write the audio onto it
    4. Play w/ ffplay
    5. Delete the temp file

    #param song: file to play
    #type Audiosegment
    """
    def ffplay_play(self):
        # Windows: close handle first or ffplay throws PermissionError
        fd, path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)

        print(tempfile.gettempdir)

        try:
            self.song.export(path, format="wav")
            subprocess.call(["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", path])
        finally:
            os.remove(path)
    

"""
    A simple test function to test pyDub features through functions

    #param filename: name of the file to playback
    #type Audiosegment

    #return: None, playback of audio should play
"""

def prompt_user():
    root = tk.Tk()
    root.withdraw()

    file = filedialog.askopenfilename(title="Select a file", filetypes=FILETYPES)

    root.destroy()

    if file:
        return AudioSegment.from_file(file)

    return None

def main():
    song = Song(prompt_user())

    print(song)

    song.ffplay_play()

    return()


if __name__ == '__main__':
    main()