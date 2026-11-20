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
import numpy as np
import librosa
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.ticker import ScalarFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
        self._proc = None
        self._tmp_path = None

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
        self.stop()

        # Windows: close handle first or ffplay throws PermissionError
        fd, path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)

        self._tmp_path = path

        self.song.export(path, format="wav")
        self._proc = subprocess.Popen(["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", path])

    """
    This function closes the ffplay process when the program is stopped
    """
    def stop(self):
        #subprocess for ffplay exists
        if self._proc is not None and self._proc.poll() is None:
            self._proc.terminate()

            #if it still exists after terminating fully kill the process
            try:
                self._proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self._proc.kill()
                self._proc.wait()

        self._proc = None

        # remove the tmp path for ffplay
        if self._tmp_path and os.path.exists(self._tmp_path):
            try:
                os.remove(self._tmp_path)
            except OSError:
                pass

        self._tmp_path = None

    def draw_matplot(self, master):
        samples, sr = self._to_librosa()
        dur = len(samples) / sr
        window_s = min(3, dur)
        peak = np.abs(samples).max()

        fig = Figure(figsize=(5, 3.5))
        wav = FigureCanvasTkAgg(fig, master=master)
        ax = fig.add_subplot(111)
        fig.subplots_adjust(bottom=.32)

        librosa.display.waveshow(samples, sr=sr, ax=ax, linewidth=0.5)
        ax.set_xlim(0, window_s)
        ax.set_ylim(-peak * 1.1, peak * 1.1)

        fmt = ScalarFormatter(useOffset=False)
        fmt.set_scientific(False)
        ax.xaxis.set_major_formatter(fmt)
        ax.set_xlabel("Time (s)")

        if (dur > window_s):
            slider_ax = fig.add_axes([.15, .14, .7, .04])
            zoom_ax = fig.add_axes([.15, .06, .7, .04])
            
            self._scroll_slider = Slider(
                slider_ax, "Time (s)", 0, dur - window_s, valinit=0, valfmt="%.1f"
            )

            self._zoom_slider = Slider(
                zoom_ax, "Position", .05, min(dur, 30), valinit=window_s, valfmt="%.2f"
            )

            def update(start):
                win = self._zoom_slider.val
                start = min(self._scroll_slider.val, dur - win)
                ax.set_xlim(start, start + win)
                fig.canvas.draw_idle()

            self._scroll_slider.on_changed(update)
            self._zoom_slider.on_changed(update)
        
        wav.draw()
        return wav  

    def _to_librosa(self):
        samples = np.array(self.song.get_array_of_samples(), dtype=np.float32)
        
        samples /= 2 ** (8 * self.song.sample_width - 1)

        if self.song.channels > 1:
            samples = samples.reshape((-1, self.song.channels)).T

            samples = librosa.to_mono(samples)

        sr = self.song.frame_rate

        return samples, sr


"""
    This functon prompts the user for an audio file by opening their file explorer
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

    song.draw_matplot()

    #song.ffplay_play()

    return()

if __name__ == '__main__':
    main()