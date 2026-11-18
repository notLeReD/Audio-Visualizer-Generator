import tkinter as tk
from tkinter import ttk
import audio as aud
from audio import Song

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Audio-Visualizer Generator")
        self.configure(background="#696969")
        self.minsize(350, 350)
        self.maxsize(850, 850)
        self.geometry("500x500+100+100")
        
        

        self.loaded_song = None

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.widgets()

    def widgets(self):
        self.load_button = tk.Button(
            self, 
            text="Load Audio", 
            command=self.on_load
        )
        
        self.load_button.pack(pady=8, padx=4)

        self.button_r2 = tk.Frame(self)

        self.play_button = tk.Button(
            self.button_r2, 
            text="Play Audio", 
            command=self.on_play
        )

        self.stop_button = tk.Button(
            self.button_r2,
            text="Stop Audio", 
            command=self.on_stop
        )

    def on_load(self):

        # stop playing audio when new song is loaded
        if self.loaded_song is not None:
            self.loaded_song.stop()
        
        self.loaded_song = Song(aud.prompt_user())
        print(self.loaded_song)
        print("Load clicked!")

        self.button_r2.pack(pady=4)
        self.play_button.pack(side ="left", padx=4)
        self.stop_button.pack(side ="left", padx=4)

    def on_play(self):
        self.loaded_song.ffplay_play()
        print("Play Clicked!")

    def on_stop(self):
        self.loaded_song.stop()
        print("Stop Clicked!")

    def on_close(self):
        if self.loaded_song is not None:
            self.loaded_song.stop()

        self.destroy()


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

