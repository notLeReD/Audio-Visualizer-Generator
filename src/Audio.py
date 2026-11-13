#TODO:
# - lookup different audio systems/handlers for python
# - possible choices: (https://wiki.python.org/python/multimedia/Audio.html)
#   - pyAudio: bindings for PortAudio input/output
#   - pyDub: audio manipulation
#   - ffmpeg: decoder, encoder, transcoder, mux, streamer

import os
import glob
import inspect
import time
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play

#change these later when implementing
DIR_AUDIO = Path(__file__).resolve().parent.parent/"audio"
EXTENSIONS = {".mp3", ".wav"}

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
    #play(chorus)

"""
    Function to list the test audios in the test audio folder

    WILL BE DEPRECATED LATER
"""
def list_audio():
    print(DIR_AUDIO)
    return sorted(
        f for f in DIR_AUDIO.iterdir()
        if f.suffix.lower() in EXTENSIONS
    )

"""
    Function to pick audios from the test audio folder

    WILL BE DEPRECATED LATER
"""
def pick_audio():
    files = list_audio()
    if not files:
        raise FileNotFoundError(f"No audio files found in {DIR_AUDIO}")

    for i, f in enumerate(files):
        print(f"{i}: {f.name}")

    while True:
        choice = int(input("Pick a file number: "))
        return AudioSegment.from_file(files[choice])

def main():

    song = pick_audio()
    playback(song)

    return()


if __name__ == '__main__':
    main()