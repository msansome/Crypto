# Simple Caesar Cipher Brut Force Decryption tool
# M Sansome June 2020
# Version 3.0.
# This version: Code redesign. Now uses the ScrollbarFrame class for the middle scrolling window

# Note: ScrollbarFrame.py and CaesarTextV2_0 both need to be
# in the same directory as this file in order for it to work.

# ToDo: Add option to load from file?

import tkinter as tk
from tkinter import scrolledtext
from Caesar.ScrollbarFrame import ScrollbarLabelFrame # Import ScrollbarFrame from https://stackoverflow.com/a/62446457/7414759
from Caesar.CaesarTextV2_0 import caesar # Import the decryption module from my text based version

class App(tk.Tk):
    """A simple GUI wrapper for the text-based Caesar Cipher decryption tool."""
    def __init__(self, title="Sample App", *args, **kwargs):
        super().__init__()

        self.title(title)

        # Create the top (input) frame:
        self.input_frame = tk.LabelFrame(self, text="Ciphertext")
        self.input_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.input_frame.columnconfigure(0, weight=1)
        self.input_frame.rowconfigure(0, weight=1)

        # Create the middle (key selection) Frame:
        # Import ScrollbarFrame from https://stackoverflow.com/a/62446457/7414759
        self.key_selection_frame = ScrollbarLabelFrame(self, text="Select which Key to use for decryption")
        self.key_selection_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.key_selection_frame.columnconfigure(0, weight=1)
        self.key_selection_frame.rowconfigure(0, weight=1)

        # Create the bottom (output) frame:
        self.output_frame = tk.LabelFrame(self, text="Plaintext")
        self.output_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.NSEW)
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)

        # Configure the three frames to resize as desired
        self.rowconfigure([0, 2], minsize=90)  # Set min size for top and bottom
        self.rowconfigure(1, weight=1)  # Row 1 should adjust to window size
        self.columnconfigure(0, weight=1)  # Column 0 should adjust to window size

        # Content for the input frame, (one label, one input box and one button).
        tk.Label(self.input_frame,
                 text="Please type, or paste, the text to be analysed into this box:").grid(row=0, columnspan=3,
                                                                                            sticky=tk.W)
        self.input_box = scrolledtext.ScrolledText(self.input_frame, height=5, wrap=tk.WORD)
        self.input_box.columnconfigure(0, weight=1)
        self.input_box.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)
        tk.Button(self.input_frame,
                  text="Decrypt",
                  command=self.draw_choices).grid(row=2, column=2, sticky=tk.E)

        # Content for the output frame, (one text box only).
        self.output_box = scrolledtext.ScrolledText(self.output_frame, width=40, height=5, wrap=tk.WORD)
        self.output_box.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)

        self.inner_proc_frame = self.key_selection_frame.scrolled_frame # Use the ScrollbarFrame class method

    def draw_choices(self):
        """ This method will display one line per key for 25 keys.
        It will draw them on the middle (scrollable) frame, and is only called
        when the Decrypt button is clicked."""
        self.key = tk.IntVar()  # Variable used to hold decryption key
        self.get_ciphertext() # get the ciphertext from the input box.
        for i in range(25): # Display one entry per key (25)
            tk.Radiobutton(self.inner_proc_frame,
                        text=f"Key = {i + 1}: ", variable=self.key,
                        value=i,
                        command=self.doDecrypt,
                        ).grid(row=i, column=0, sticky=tk.W)
            tk.Label(self.inner_proc_frame,
                  text=caesar(self.shortText, i + 1, True),
                  bg="WHITE",
                  anchor=tk.W
                  ).grid(row=i, column=1, sticky=tk.W)

    def get_ciphertext(self):
        """ Will get the ciphertext from the input box and also create a shortened version to display on one line"""
        screenWidth = 78
        self.ciphertext = self.input_box.get(0.0, tk.END)

        if len(self.ciphertext) > screenWidth:
            self.shortText = self.ciphertext[:screenWidth]
        else:
            self.shortText = self.ciphertext[:]
        self.shortText = self.shortText.replace('\n', ' ') # strip out carriage returns just in case


    def doDecrypt(self):
        """This will ultimately decrypt and display the results"""
        key = self.key.get() # Get key from radio button press
        output_txt = caesar(self.ciphertext, key + 1, True)
        self.output_box.delete(0.0,tk.END)
        self.output_box.insert(0.0, output_txt)


if __name__ == "__main__":
    App("Caesar Cipher - Brute Force Decryption Tool").mainloop()