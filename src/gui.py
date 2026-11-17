import tkinter as tk
from tkinter import ttk
import audio as aud

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Audio-Visualizer Generator")
        self.configure(background="#696969")
        self.minsize(350, 350)
        self.maxsize(850, 850)
        self.geometry("500x500+100+100")
        self.loaded_song = None

        self.widgets()

    def widgets(self):
        self.load_button = tk.Button(
            self, 
            text="Load Audio", 
            command=self.on_load
        )
        
        self.load_button.pack(pady=10)

        self.play_button = tk.Button(
            self, 
            text="Play Audio", 
            command=self.on_play
        )

        self.play_button.pack(pady=10)

    def on_load(self):
        self.loaded_song = aud.prompt_user()
        print(self.loaded_song)
        print("Load clicked!")

    def on_play(self):
        aud.ffplay_play(self.loaded_song)
        print("Play Clicked!")


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

