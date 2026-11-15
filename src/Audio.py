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

"""
    A simple test function to test pyDub features through functions

    #param filename: name of the file to playback
    #type Audiosegment

    #return: None, playback of audio should play
"""
def playback(audio):

    chorus_start = 36 * 1000
    chorus_end = 64 * 1000

    chorus = audio[chorus_start:chorus_end]

    chorus = chorus.fade_in(2000).fade_out(3000)

    params = {k: v for k, v in vars(chorus).items() if k != "_data"}
    print(params)
    ffplay_play(chorus)

def ffplay_play(audio):
    subprocess.call(["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", audio])

def prompt_user():
    root = tk.Tk()
    root.withdraw()

    file = filedialog.askopenfilename(title="Select a file", filetypes=FILETYPES)

    root.destroy()

    if file:
        return file

    return None

def print_attrb(file):

    song = AudioSegment.from_file(file)

    print(song.channels, song.frame_rate, song.sample_width)
    print(song.dBFS, song.max, song.max_possible_amplitude, len(song))

def main():
    song = prompt_user()

    ffplay_play(song)

    return()


if __name__ == '__main__':
    main()