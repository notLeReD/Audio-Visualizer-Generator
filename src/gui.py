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

        self.widgets()

    def widgets(self):
        self.load_button = tk.Button(
            self, 
            text="Load Audio", 
            command=self.on_load
        )
        
        self.load_button.pack(padx=200, pady=200)

    def on_load(self):
        aud.prompt_user()
        print ("Load clicked!")


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

