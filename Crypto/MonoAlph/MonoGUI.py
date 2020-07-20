# An application to assist in the encryption and decryption of simple
# monaalphabetic substitution ciphers.

# M. Sansome June 2020
# Version 1.0

# Version History
# ===============
# v0.0 Basic tkinter structure constructed
# v0.1 Inclusion of automated break algorithm plus improved alphabet entry events
# v0.2 Addition of copy to keyboard facility
# v0.3 Addition of "Import Key" functionality plus code tidy-up
# v0.4 Inclusion of pattern matching decryption
# v0.4.1 Create inverted key functionality added
# v0.4.3 Inclusion of threading for Auto Decrypt
# v0.5 Basic Frequency Analysis added - not yet complete
# v0.5.1 Improved version of Frequency Analysis plots
# v0.5.2 Finished version of Frequency Analysis plots
# v0.5.3 Added Index of Coincidence method
# v0.5.4 Added Double Letters analysis tool
# v1.0 First release version - most features now added

# ToDo: Add ability to click on text and directly change cipher alphabet.


import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from random import shuffle
from threading import Thread
import os
# import wordPatterns, makeWordPatterns
no_matplot_message = 'Sorry - you do not have the Matplotlib Libraries installed.\nYou will not be able to see ' \
                     'Frequency Analysis graphically.\n\nTry "pip install matplotib" - or see your system ' \
                     'administrator '
try:
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    matplot_installed = True
except ModuleNotFoundError:
    tk.messagebox.showwarning("Warning", no_matplot_message)
    matplot_installed = False
import simpleSubPatternHack as ss_hack
from Cryptanalysis import Cryptanalyse as Crypto  # My crypto tools
# Hill-climbing algorithm adapted from Practical Cryptography
from break_simplesub import Mono_break as mb


class App(tk.Tk):
    def __init__(self, title="Sample App", *args, **kwargs):
        super().__init__()
        self.title(title)
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.ciphertext = ""
        self.alphabet_dict = {}
        self.output_key = ""

        # Create the top (input) frame:
        self.input_frame = tk.LabelFrame(self, text="Ciphertext")
        self.input_frame.grid(row=0, column=0, columnspan=3,
                              padx=5, pady=5, sticky=tk.NSEW)
        self.input_frame.columnconfigure(0, weight=1)
        self.input_frame.rowconfigure(0, weight=1)

        # Create the middle (alphabet) frame:
        self.alphabet_frame = tk.LabelFrame(self, text="The Alphabet")
        self.alphabet_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.alphabet_frame.columnconfigure(0, weight=1)
        self.alphabet_frame.rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create the middle (Analysis tools) frame:
        self.analysis_tools_frame = tk.LabelFrame(self, text="Analysis Tools")
        self.analysis_tools_frame.grid(
            row=1, column=1, padx=5, pady=5, sticky=tk.NW)
        self.analysis_tools_frame.columnconfigure(0, weight=1)
        self.analysis_tools_frame.rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create the middle (Key tools) frame:
        self.key_tools_frame = tk.LabelFrame(self, text="Key Tools")
        self.key_tools_frame.grid(
            row=1, column=2, padx=5, pady=5, sticky=tk.NSEW)
        self.key_tools_frame.columnconfigure(0, weight=1)
        self.key_tools_frame.rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create the bottom (output) frame:
        self.output_frame = tk.LabelFrame(self, text="Plaintext")
        self.output_frame.grid(row=2, column=0, columnspan=3,
                               padx=5, pady=5, sticky=tk.NSEW)
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)

        # Set min size for top and bottom
        self.rowconfigure([0, 2], minsize=90)
        self.rowconfigure(1, weight=1)  # Row 1 should adjust to window size
        # Column 0 should adjust to window size
        self.columnconfigure(0, weight=1)

        # Content for the input frame
        tk.Label(self.input_frame,
                 text="Please type, or paste, the text to be analysed into this box:").grid(row=0, columnspan=3,
                                                                                            sticky=tk.W)
        self.input_box = scrolledtext.ScrolledText(
            self.input_frame, height=8, wrap=tk.WORD)
        self.input_box.columnconfigure(0, weight=1)
        self.input_box.grid(row=1, column=0, columnspan=7, sticky=tk.NSEW)
        ttk.Button(self.input_frame,
                   text="Load from File",
                   command=self.fileDialog).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Button(self.input_frame,
                   text="Encrypt/Decrypt",
                   command=self.enc_dec).grid(row=2, column=2, padx=5, pady=5, sticky=tk.E)
        ttk.Button(self.input_frame,
                   text="Pattern Decrypt",
                   command=self.pattern_decrypt).grid(row=2, column=3, padx=5, pady=5, sticky=tk.E)
        ttk.Button(self.input_frame,
                   text="Auto Decrypt",
                   command=self.create_auto_decrypt_window).grid(row=2, column=4, padx=5, pady=5, sticky=tk.E)

        # Content for the analysis tools frame
        ttk.Button(self.analysis_tools_frame,
                   text="Index of Coincidence",
                   command=self.create_ic_window).grid(row=0, column=0, padx=2, pady=2, sticky=tk.NW)
        ttk.Button(self.analysis_tools_frame,
                   text="Frequency Analysis",
                   command=self.create_freq_analysis_window).grid(row=1, column=0, padx=2, pady=2, sticky=tk.NW)
        ttk.Button(self.analysis_tools_frame,
                   text="Doubles Analysis",
                   command=self.create_double_letters_window).grid(row=2, column=0, padx=2, pady=2, sticky=tk.NW)

        # Content for the key tools frame
        ttk.Button(self.key_tools_frame,
                   text="Random Key",
                   command=self.random_alphabet).grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
        ttk.Button(self.key_tools_frame,
                   text="Copy Key to Clipboard",
                   command=self.copy_key_to_clipboard).grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
        ttk.Button(self.key_tools_frame,
                   text="Import Key",
                   command=self.create_key_import_window).grid(row=2, column=0, padx=2, pady=2, sticky=tk.W)
        ttk.Button(self.key_tools_frame,
                   text="Invert Key",
                   command=self.inv_key).grid(row=3, column=0, padx=2, pady=2, sticky=tk.W)
        ttk.Button(self.key_tools_frame,
                   text="Reset Key",
                   command=self.make_blank_alphabet).grid(row=4, column=0, padx=2, pady=2, sticky=tk.W)

        # Content for the output frame, (one text box only).
        self.output_box = scrolledtext.ScrolledText(
            self.output_frame, width=40, height=8, wrap=tk.WORD)
        self.output_box.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)
        ttk.Button(self.output_frame,
                   text="Copy to Clipboard",
                   command=self.copy_output_to_clipboard).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.create_alphabet_entry_boxes()
        self.make_blank_alphabet()

    def make_blank_alphabet(self):
        # Fill the dictionary with *'s
        for i in range(26):
            self.alphabet_dict[self.alphabet[i]] = "*"
        self.draw_key()

    def make_dict_from_key(self):  # Use the method in the Cryptanalysis class
        self.alphabet_dict = Crypto(
            self.ciphertext, self.key).make_dictionary_from_key()

    def make_key_from_dict(self):
        # Creates a 26 character string of the key
        # We can't just invert the dictionary, because missing letters would cause an error
        # so we have to find which letters are missing and add them as * to the key.

        missing_letters = []
        # Create lists of the keys and values
        key_list = list(self.alphabet_dict.keys())
        val_list = list(self.alphabet_dict.values())
        for letter in self.alphabet:
            if letter not in val_list:
                missing_letters.append(letter)
        for i in range(26):
            if val_list[i] not in self.alphabet:
                cletter = "*"
            else:
                cletter = key_list[i]
            self.output_key += cletter

    def inv_key(self):
        # Not currently used
        inverted_dict = {v: k for k, v in self.alphabet_dict.items()}
        # print(self.alphabet_dict)
        self.alphabet_dict = inverted_dict
        # print(self.alphabet_dict)
        # print(inverted_dict)
        self.draw_key()

    def create_alphabet_entry_boxes(self):
        # This method will run through and create all the labels and entry boxes
        # for the 26 letters of the alphabet in a loop (and store the entry objects in a list)
        self.entries = []  # Empty list to store entry objects
        for i in range(26):  # Display each letter and an entry box to enter letter
            tk.Label(self.alphabet_frame,
                     text=self.alphabet[i]
                     ).grid(row=0, column=i, padx=1, pady=1, sticky=tk.W)
            entry = tk.Entry(self.alphabet_frame, width=1,
                             name=f"letter{self.alphabet[i]}")
            entry.grid(row=1, column=i, padx=1, pady=1, sticky=tk.W)
            entry.bind("<FocusIn>", self.handleIN)
            entry.bind("<Return>", self.handleOut)
            entry.bind("<FocusOut>", self.handleOut)
            entry.bind("<Escape>", self.handle_esc)
            entry.bind("<Delete>", self.handle_del)
            entry.bind("<BackSpace>", self.handle_del)
            # write the object into the list for later access
            self.entries.append(entry)

    def draw_key(self):
        # Draw the Alphabet from the dictionary
        # print("In Draw Key. Key is:", self.key)
        for i in range(26):
            self.entries[i].delete(0, tk.END)
            self.entries[i].insert(0, self.alphabet_dict[self.alphabet[i]])

    def enc_dec(self):
        # This method will apply the key to the ciphertext and write the output into the output box
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
                # Skip stuff like punctuation etc.
                self.plaintext += self.ciphertext[j]
        self.output_box.delete(0.0, tk.END)
        self.output_box.insert(0.0, self.plaintext)

    def auto_break(self):
        # This will instantiate a Mono_break object from the Mono_break class imported break_simplesub_3
        # and try to perform a hill-climbing algorithm attack on the cipher.
        # Uses threading to detach the process
        self.ciphertext = self.input_box.get(0.0, tk.END)
        self.auto_break_obj = mb(self.ciphertext)
        self.control_thread = Thread(
            target=self.auto_break_obj.do_break, daemon=True, args=(self.progress,))
        message = "Loading Dictionaries...\n"
        self.auto_decrypt_output.delete(0.0, tk.END)
        self.auto_decrypt_output.insert(0.0, message)
        self.control_thread.start()

    def stop_auto_break(self):
        self.auto_break_obj.stopped = True
        self.make_dict_from_key()
        self.draw_key()
        self.plaintext = Crypto(self.ciphertext, self.key).decipher()
        self.output_box.delete(0.0, tk.END)
        self.output_box.insert(0.0, self.plaintext)
        self.auto_decrypt_window.destroy()

    def progress(self, message, key):
        self.message = message
        self.key = key
        self.auto_decrypt_output.insert(tk.END, self.message)

    def pattern_decrypt(self):
        self.ciphertext = self.input_box.get(0.0, tk.END)
        letterMapping = ss_hack.hackSimpleSub(self.ciphertext)
        self.key = ss_hack.decryptWithCipherletterMapping(
            self.ciphertext, letterMapping)
        self.make_dict_from_key()
        self.draw_key()
        self.plaintext = Crypto(self.ciphertext, self.key).decipher()
        self.output_box.delete(0.0, tk.END)
        self.output_box.insert(0.0, self.plaintext)

    def copy_to_clipboard(self, output):
        # Main Copy to clipboard method (takes the desired item as a parameter)
        self.clipboard_clear()
        self.clipboard_append(output)
        self.update()  # now it stays on the clipboard after the window is closed

    def copy_key_to_clipboard(self):
        # Copy the key to the clipboard
        self.make_key_from_dict()
        outkey = self.output_key
        self.copy_to_clipboard(outkey)

    def copy_output_to_clipboard(self):
        # Copy the output to the clipboard
        out_txt = self.output_box.get(0.0, tk.END)
        self.copy_to_clipboard(out_txt)

    def import_key(self):
        # Called from the Import Key button on the spawned Import Key window
        self.key = self.key_import_entry.get()
        self.make_dict_from_key()
        self.draw_key()
        self.enc_dec()
        self.key_import_window.destroy()

    def print_values(self):
        # Will cycle though the letter entry boxes and return their contents
        # (not currently used)
        for entry in self.entries:
            print(entry, entry.get())

    def handleIN(self, event):
        # Method triggered by event when cursor clicked in entry box
        # Find which letter we're in by referencing the widget name
        letter = str(event.widget)
        # Get the actual letter by looking at the last character of the widget name
        self.letterpos = letter[-1]
        self.current_letter = self.alphabet_dict[self.letterpos]
        event.widget.delete(0, tk.END)

    def handleOut(self, event):
        # Method triggered by event when cursor clicked out of entry box
        typed = event.widget.get()
        if typed.isalpha() and len(typed) == 1:
            typed = typed.upper()
            inverted_dict = {v: k for k, v in
                             self.alphabet_dict.items()}  # create an inverted dictioanry to look up position
            if typed in self.alphabet_dict.values() and inverted_dict[typed] != self.letterpos:
                message = f"Careful! You've used {typed} already at {inverted_dict[typed]}!"
                tk.messagebox.showwarning("Warning", message)
                typed = "*"
        elif typed == "":
            typed = self.current_letter
        else:
            typed = "*"
        event.widget.delete(0, tk.END)
        event.widget.insert(0, typed)
        self.alphabet_dict[self.letterpos] = typed
        self.enc_dec()
        self.output_box.delete(0.0, tk.END)
        # Redraw the modified plaintext
        self.output_box.insert(0.0, self.plaintext)

    def handle_esc(self, event):
        # Method triggered by event when escape pressed when in entry box
        event.widget.delete(0, tk.END)
        event.widget.insert(0, self.current_letter)

    def handle_del(self, event):
        # Method triggered by event when delete key pressed when in entry box
        event.widget.delete(0, tk.END)
        event.widget.insert(0, "*")
        self.alphabet_dict[self.letterpos] = "*"
        return "break"

    def random_alphabet(self):
        # Will create a random key and draw it into the display
        new_alphabet = list(self.alphabet)
        shuffle(new_alphabet)
        self.key = "".join(new_alphabet)
        self.make_dict_from_key()
        self.draw_key()

    def create_key_import_window(self):
        # New window spawned when "Import Key" button is clicked
        self.key_import_window = tk.Toplevel(self)
        self.key_import_window.title("Key Import")
        self.key_import_frame = tk.LabelFrame(
            self.key_import_window, text="Key Import")
        self.key_import_frame.grid(
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
        self.key_import_frame.columnconfigure(0, weight=1)
        self.key_import_frame.rowconfigure(0, weight=1)
        key_import_label = ttk.Label(self.key_import_frame,
                                     text="Please type or paste the key \n(as a 26 character string - all uppercase)")
        self.key_import_entry = tk.Entry(self.key_import_frame, width=36)
        key_import_button = ttk.Button(
            self.key_import_frame, text="Import Key", command=self.import_key)
        key_import_cancel_button = ttk.Button(self.key_import_frame, text="Cancel",
                                              command=lambda: self.key_import_window.destroy())
        key_import_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.key_import_entry.grid(
            row=1, column=0, columnspan=2, padx=5, pady=5)
        key_import_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        key_import_cancel_button.grid(
            row=2, column=1, padx=5, pady=5, sticky=tk.E)

    def create_auto_decrypt_window(self):
        # New window spawned when "Import Key" button is clicked
        self.auto_decrypt_window = tk.Toplevel(self)
        self.auto_decrypt_window.title(
            "Attempt Automatic Decrypt Using Hill-Climbing Algorithm")
        self.auto_decrypt_frame = tk.LabelFrame(
            self.auto_decrypt_window, text="Automatic Decrypt")
        self.auto_decrypt_frame.grid(
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
        self.auto_decrypt_frame.columnconfigure(0, weight=1)
        self.auto_decrypt_frame.rowconfigure(0, weight=1)
        auto_decrypt_label = ttk.Label(self.auto_decrypt_frame,
                                       text="Please press start to begin - Press STOP when a likely answer is revealed.")
        # self.auto_decrypt_output = tk.Text(self.auto_decrypt_frame, width=36)
        self.auto_decrypt_output = scrolledtext.ScrolledText(
            self.auto_decrypt_frame, height=10, wrap=tk.WORD)
        self.auto_decrypt_output.columnconfigure(0, weight=1)
        self.auto_decrypt_output.grid(
            row=1, column=0, columnspan=5, sticky=tk.NSEW)
        auto_decrypt_start_button = ttk.Button(self.auto_decrypt_frame, text="Start Decrypt",
                                               command=self.auto_break)
        auto_decrypt_cancel_button = ttk.Button(self.auto_decrypt_frame, text="Cancel",
                                                command=lambda: self.auto_decrypt_window.destroy())
        auto_decrypt_stop_button = ttk.Button(self.auto_decrypt_frame, text="Stop!",
                                              command=self.stop_auto_break)
        auto_decrypt_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.auto_decrypt_output.grid(
            row=1, column=0, columnspan=3, padx=5, pady=5)
        auto_decrypt_start_button.grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W)
        auto_decrypt_stop_button.grid(
            row=2, column=1, padx=5, pady=5, sticky=tk.W)
        auto_decrypt_cancel_button.grid(
            row=2, column=2, padx=5, pady=5, sticky=tk.E)
        message = """This tool will attempt to break the Substitution Cipher.

It may take several iterations and might take some to to complete.
Press "Start" to begin, and when a satisfactory answer is produced,
press "Stop" to return to the main program."""
        self.auto_decrypt_output.insert(0.0, message)

    def create_freq_analysis_window(self):
        # New window spawned when "Frequency Analysis" button is clicked
        self.ciphertext = self.input_box.get(0.0, tk.END)
        # Instantiate a Crypto object with current text
        self.cryptanalysis = Crypto(self.ciphertext)
        self.freq_analysis_window = tk.Toplevel(self)
        self.freq_analysis_window.title("Frequency Analysis")
        self.freq_analysis_frame = tk.LabelFrame(
            self.freq_analysis_window, text="Letter Frequencies")
        self.freq_analysis_frame.grid(
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
        self.freq_analysis_frame.columnconfigure(0, weight=1)
        self.freq_analysis_frame.rowconfigure(0, weight=1)
        ttk.Label(self.freq_analysis_frame,
                  text="Letter Frequency in English:").grid(row=0, column=0, columnspan=7,
                                                            padx=5, pady=5, sticky=tk.NSEW)
        # Get the standard English frequencies from the Cryptanalysis class and sort them into descending order
        sorted_eng_freqs = self.sort_dict(self.cryptanalysis.std_Eng_freqs)
        depth = 4  # arrange layout on page (depth = no. of rows)
        for j in range(depth):
            for i in range(j, len(sorted_eng_freqs), depth):
                ttk.Label(self.freq_analysis_frame,
                          text=f'{i + 1:02} : {sorted_eng_freqs[i][0]} : {sorted_eng_freqs[i][1]:6.3f}',
                          font='TkFixedFont', relief="groove", borderwidth=1
                          ).grid(row=j + 1, column=i // depth, padx=1, pady=1, sticky=tk.W)
        # Use the frequencies method of Crypto to get the letter frequencies
        ctext_freqs = self.cryptanalysis.frequencies()
        self.plot_freqs(ctext_freqs)
        if matplot_installed:
            f = Figure(figsize=(5, 5), dpi=100)
            a = f.add_subplot(111)
            a.bar(range(26), self.letter_freqs)
            a.set_xticks(range(26))
            a.set_xticklabels([x for x in self.alphabet])
            a.set_title("Frequency of each letter (%)")

            canvas = FigureCanvasTkAgg(f, self.freq_analysis_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0)
            # toolbar = NavigationToolbar2Tk(canvas,self.freq_analysis_frame).grid(row=1, column=0)
            # toolbar.update()
            canvas._tkcanvas.grid(row=2 + depth, column=0, columnspan=7)
        else:
            tk.messagebox.showwarning("Warning", no_matplot_message)
        ttk.Label(self.freq_analysis_frame,
                  text="Letter Frequency in Ciphertext:"
                  ).grid(row=3 + depth, column=0, columnspan=7, padx=5, pady=5, sticky=tk.NSEW)
        ctext_freqs = self.sort_dict(ctext_freqs)
        for j in range(depth):
            for i in range(j, len(ctext_freqs), depth):
                tk.Label(self.freq_analysis_frame,
                         text=f'{i + 1:02} : {ctext_freqs[i][0]} : {ctext_freqs[i][1]:6.3f}', font='TkFixedFont',
                         relief="groove", borderwidth=1
                         ).grid(row=j + 8, column=i // depth, padx=1, pady=1, sticky=tk.W)

    def create_double_letters_window(self):
        # New window spawned when "Double Letters" button is clicked
        self.ciphertext = self.input_box.get(0.0, tk.END)
        # Instantiate a Crypto object with current text
        self.cryptanalysis = Crypto(self.ciphertext)
        self.double_letters_window = tk.Toplevel(self)
        self.double_letters_window.title("Double Letters")
        self.double_letters_frame = tk.LabelFrame(
            self.double_letters_window, text="Double Letters")
        self.double_letters_frame.grid(
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
        self.double_letters_frame.columnconfigure(0, weight=1)
        self.double_letters_frame.rowconfigure(0, weight=1)
        ttk.Label(self.double_letters_frame,
                  text="The most commonly occurring double letters in English are:").grid(row=0, column=0, columnspan=7,
                                                                                          padx=5, pady=5, sticky=tk.NSEW)
        # Get the standard English double letters from the Cryptanalysis class and sort them into descending order
        # Use the Count Doubles method of Crypto to get the double-letter frequencies
        eng_double_letters = self.cryptanalysis.std_Eng_doubles
        double_letter_label_text = ''
        for i in eng_double_letters:
            double_letter_label_text = double_letter_label_text + f'{i} '
        ttk.Label(self.double_letters_frame,
                  text=double_letter_label_text).grid(row=1, column=0, columnspan=7, padx=5, pady=5, sticky=tk.NSEW)
        ctext_freqs = self.cryptanalysis.count_doubles()
        self.plot_freqs(ctext_freqs)
        if matplot_installed:
            f = Figure(figsize=(5, 5), dpi=100)
            a = f.add_subplot(111)
            a.bar(range(26), self.letter_freqs)
            a.set_xticks(range(26))
            a.set_xticklabels([x for x in self.alphabet])
            a.set_title("Frequency of each letter (Count)")

            canvas = FigureCanvasTkAgg(f, self.double_letters_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0)
            # toolbar = NavigationToolbar2Tk(canvas,self.double_letters_frame).grid(row=1, column=0)
            # toolbar.update()
            canvas._tkcanvas.grid(row=2, column=0, columnspan=7)
        else:
            tk.messagebox.showwarning("Warning", no_matplot_message)
        ttk.Label(self.double_letters_frame,
                  text="Double-Letter Frequency in Ciphertext:"
                  ).grid(row=3, column=0, columnspan=7, padx=5, pady=5, sticky=tk.NSEW)
        ctext_freqs = self.sort_dict(ctext_freqs)
        ctext_double_letter_label_text = ''
        for i in ctext_freqs:
            ctext_double_letter_label_text = ctext_double_letter_label_text + \
                f'{i[0]*2} (x{i[1]})  '
        ttk.Label(self.double_letters_frame, text=ctext_double_letter_label_text,
                  font='TkFixedFont', relief="groove", borderwidth=1).grid(row=4, column=0, padx=1, pady=1, sticky=tk.W)

    def create_ic_window(self):
        # New window spawned when "Index of Coincidence" button is clicked
        self.ciphertext = self.input_box.get(0.0, tk.END)
        # Instantiate a Crypto object with current text
        self.cryptanalysis = Crypto(self.ciphertext)
        self.ic_window = tk.Toplevel(self)
        self.ic_window.title("Index of Coincidence")
        self.ic_frame = tk.LabelFrame(self.ic_window, text="IC")
        self.ic_frame.grid(row=0, column=0, columnspan=2,
                           padx=5, pady=5, sticky=tk.NSEW)
        self.ic_frame.columnconfigure(0, weight=1)
        self.ic_frame.rowconfigure(0, weight=1)
        ic_explanation = '''        The 'Index of Coincidence' (IC).
           This is a measure of how similar a frequency distribution is to the
           uniform distribution (or how 'spiky' it is. The I.C. of a piece of text does not
           change if the text is enciphered with a substitution cipher. In other words,
           regular English will have an IC of around 0.066, and so will a piece of
           ciphertext enciphered with a substitution cipher. However, a polyalphabetic
           cipher (e.g. a Vigenere cipher) will have an IC of around 0.038.
           \n'''
        ttk.Label(self.ic_frame, text=ic_explanation).grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        # Use the ic method of Crypto to get the Index of Coincidence for this text.
        ic = round(self.cryptanalysis.ic(), 3)
        ic_calc_message = f'The Index of Coincidence for this text is {ic}.'
        ttk.Label(self.ic_frame, text=ic_calc_message, font='TkDefaultFont 13 bold', relief="groove",
                  borderwidth=3, padding=(5, 5, 5, 5)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

    def fileDialog(self):
        # Method which invokes the inport file dialogue
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select A File", filetypes=[
            ("TXT", "*.txt"),
            ("All files", "*")])
        with open(self.filename) as input_file:
            self.input_box.delete(0.0, tk.END)
            self.input_box.insert(0.0, input_file.read())

    def plot_freqs(self, ctext_freqs):
        # Get the letter frequencies and prepare them for plotting
        # Turn the dictionary into a list and if letters are missing, give them a count of 0
        self.letter_freqs = []
        for letter in self.alphabet:
            try:
                self.letter_freqs.append(ctext_freqs[letter])
            except KeyError:
                self.letter_freqs.append(0)

    def sort_dict(self, dict):
        # This will sort a dictionary (e.g. letter frequencies) in descending order by value
        sorted_dict = sorted(dict.items(), key=lambda y: y[1], reverse=True)
        return sorted_dict


if __name__ == "__main__":
    App("Simple Substitution Cipher Tool").mainloop()
