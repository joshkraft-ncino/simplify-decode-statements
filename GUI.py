import tkinter as tk

class SeaofBTCapp(tk.Tk):   # Inherit from TK

    def __init__(self, *args, **kwargs):          # Always runs when class is initiated

        tk.Tk.__init__(self, *args, **kwargs)     # Initialize tkinter as well
        container = tk.Frame(self)                # Frame = edge of window

        container.pack(side="top", fill="both", expand=True) # Expand to fill all white space

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}            # dictionary that holds frames to allow switching

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky = "nsew")    # grid is better version of PACK
