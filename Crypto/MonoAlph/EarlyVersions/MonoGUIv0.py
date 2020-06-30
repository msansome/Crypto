# An application to assist in the encryption and decryption of simple
# monaalphabetic substitution ciphers.
# M. Sansome June 2020
# Version 0.2

#Version History
#===============
# v0.0 Basic tkinter structure constructed
# v0.1 Inclusion of automated break algorithm plus improved alphabet entry events
# v0.2 Addition of copy to keyboard facility

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from random import shuffle
import os
from CryptanalysisV02 import Cryptanalyse as Crypto # My crypto tools
from break_simplesub_3 import Mono_break as mb # Hill-climbing algorithm adapted from Practical Cryptography

class App(tk.Tk):
    def __init__(self, title="Sample App", *args, **kwargs):
        super().__init__()

        self.title(title)
        self.key = "*" * 26
        self.initialise_dictionaries()

        # Create the top (input) frame:
        self.input_frame = tk.LabelFrame(self, text="Ciphertext")
        self.input_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
        self.input_frame.columnconfigure(0, weight=1)
        self.input_frame.rowconfigure(0, weight=1)

        # Create the middle (alphabet) frame:
        self.alphabet_frame = tk.LabelFrame(self, text="The Alphabet")
        self.alphabet_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.alphabet_frame.columnconfigure(0, weight=1)
        self.alphabet_frame.rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create the middle (tools) frame:
        self.tools_frame = tk.LabelFrame(self, text="Tools")
        self.tools_frame.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
        self.tools_frame.columnconfigure(0, weight=1)
        self.tools_frame.rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create the bottom (output) frame:
        self.output_frame = tk.LabelFrame(self, text="Plaintext")
        self.output_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.NSEW)
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)

        self.rowconfigure([0, 2], minsize=90)  # Set min size for top and bottom
        self.rowconfigure(1, weight=1)  # Row 1 should adjust to window size
        self.columnconfigure(0, weight=1)  # Column 0 should adjust to window size

        # Content for the input frame, (one label, one input box and one button).
        tk.Label(self.input_frame,
                 text="Please type, or paste, the text to be analysed into this box:").grid(row=0, columnspan=3,
                                                                                            sticky=tk.W)
        self.input_box = scrolledtext.ScrolledText(self.input_frame, height=8, wrap=tk.WORD)
        self.input_box.columnconfigure(0, weight=1)
        self.input_box.grid(row=1, column=0, columnspan=5, sticky=tk.NSEW)
        ttk.Button(self.input_frame,
                   text="Load from File",
                   command=self.fileDialog).grid(row=2, column=0, sticky=tk.W)
        ttk.Button(self.input_frame,
                   text="Encrypt/Decrypt",
                   command=self.encDec).grid(row=2, column=2, padx=5, pady=5, sticky=tk.E)
        ttk.Button(self.input_frame,
                   text="Auto Decrypt",
                   command=self.auto_break).grid(row=2, column=4, padx=5, pady=5, sticky=tk.E)

        # Content for the tools frame
        ttk.Button(self.tools_frame,
                   text="Random Alphabet",
                   command=self.random_alphabet).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(self.tools_frame,
                   text="Copy Key to Clipboard",
                   command=self.copy_key_to_clipboard).grid(row=1, column=0, sticky=tk.W)

        # Content for the output frame, (one text box only).
        self.output_box = scrolledtext.ScrolledText(self.output_frame, width=40, height=8, wrap=tk.WORD)
        self.output_box.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)

        self.draw_alphabet()

    def initialise_dictionaries(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.alphabet_dict = {}
        for i in range(26):
            self.alphabet_dict[self.alphabet[i]] = self.key[i]

    def draw_alphabet(self):
        self.entries = []
        for i in range(26): # Display each letter and an entry box to enter letter
            tk.Label(self.alphabet_frame,
                        text=self.alphabet[i]
                        ).grid(row=0, column=i, padx=1, pady=1, sticky=tk.W)
            entry = tk.Entry(self.alphabet_frame, width=1, name=f"letter{self.alphabet[i]}")
            entry.insert(0,self.alphabet_dict[self.alphabet[i]])
            entry.grid(row=1, column=i, padx=1, pady=1, sticky=tk.W)
            entry.bind("<FocusIn>", self.handleIN)
            entry.bind("<Return>",self.handleOut)
            entry.bind("<FocusOut>", self.handleOut)
            entry.bind("<Escape>", self.handle_esc)
            entry.bind("<Delete>", self.handle_del)
            entry.bind("<BackSpace>", self.handle_del)
            self.entries.append(entry)

    def draw_key(self):
        # Draw the Alphabet from the key
        i = 0
        for entry in self.entries:
            entry.delete(0, tk.END)
            entry.insert(0, self.key[i])
            i += 1

    def draw_key2(self):
        # Draw the Alphabet from the dictionary
        for i in range(26):
            self.entries[i].delete(0, tk.END)
            self.entries.insert[i](0, self.alphabet_dict[self.alphabet[i]])

    def make_key_for_export(self):
        self.output_key = ""
        for i in range(26):
            self.output_key += self.alphabet_dict[self.alphabet[i]]

    def encDec(self):
        self.ciphertext = self.input_box.get(0.0, tk.END)
        self.plaintext = ""
        for j in range(len(self.ciphertext)):
            cLetter = self.ciphertext[j].upper()
            if cLetter in self.alphabet:
                pLetter = self.alphabet_dict[cLetter]
                if self.ciphertext[j].islower():
                    pLetter = pLetter.lower()
                self.plaintext += pLetter
            else:
                self.plaintext += self.ciphertext[j]
        self.output_box.delete(0.0, tk.END)
        self.output_box.insert(0.0, self.plaintext)

    def auto_break(self):
        print("Going to delete")
        self.output_box.delete(0.0, tk.END)
        print("Should have deleted")
        message = "\nThis could take some time. Please be Patient."
        print(message)
        self.output_box.insert(0.0, message)
        self.ciphertext = self.input_box.get(0.0, tk.END)
        self.key = mb(self.ciphertext).bestkey
        self.initialise_dictionaries()
        self.draw_alphabet()
        output_txt = Crypto(self.ciphertext, self.key).decipher()
        self.output_box.delete(0.0, tk.END)
        self.output_box.insert(0.0, output_txt)

    def stop(self):
        mb.stopped = True

    def copy_key_to_clipboard(self):
        self.make_key_for_export()
        self.clipboard_clear()
        self.clipboard_append(self.output_key)
        self.update()  # now it stays on the clipboard after the window is closed

    def print_values(self):
        for entry in self.entries:
            print(entry, entry.get())

    def handleIN(self,event):
        letter = str(event.widget) # Find which letter we're in by referencing the widget name
        self.letterpos = letter[-1] # Get the actual letter by looking at the last character of the widget name
        self.current_letter = self.alphabet_dict[self.letterpos]
        event.widget.delete(0, tk.END)

    def handleOut(self, event):
        typed = event.widget.get()
        if typed.isalpha() and len(typed)==1:
            typed = typed.upper()
            inverted_dict = {v: k for k, v in self.alphabet_dict.items()} #create an inverted dictioanry to look up position
            if typed in self.alphabet_dict.values() and inverted_dict[typed] != self.letterpos:
                message = f"Careful! You've used {typed} already at {inverted_dict[typed]}!"
                tk.messagebox.showwarning("Warning",message)
                typed = "*"
        elif typed =="":
            typed = self.current_letter
        else:
            typed = "*"
        event.widget.delete(0, tk.END)
        event.widget.insert(0, typed)
        self.alphabet_dict[self.letterpos] = typed
        self.encDec()
        self.output_box.delete(0.0, tk.END)
        self.output_box.insert(0.0, self.plaintext) # Redraw the modified plaintext

    def handle_esc(self, event):
        event.widget.delete(0, tk.END)
        event.widget.insert(0, self.current_letter)

    def handle_del(self, event):
        event.widget.delete(0, tk.END)
        event.widget.insert(0, "*")
        self.alphabet_dict[self.letterpos] = "*"
        return "break"

    def random_alphabet(self):
        new_alphabet = list(self.alphabet)
        shuffle(new_alphabet)
        self.key = "".join(new_alphabet)
        self.initialise_dictionaries()
        self.draw_key()

    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select A File", filetypes=[
        ("TXT", "*.txt"),
        ("All files", "*")])
        with open(self.filename) as input_file:
            self.input_box.delete(0.0,tk.END)
            self.input_box.insert(0.0, input_file.read())



if __name__ == "__main__":
    App("Simple Substitution Cipher Tool").mainloop()
