# A GUI wrapper around the Cracking Codes Book
# - https://www.nostarch.com/crackingcodes/ (BSD Licensed)
#  Public Key Encryption / Decryption program.
# Note: the uses a "textbook" implementation of the RSA algorithm which
# is effective, but not safe against a professional cryptanalitic attack.
# (see the warning message)

# Public Key Encryption / Decryption.

# M. Sansome July 2020
# Version 0.2

# Version History
# ===============
# v0.0 Just the outline structure
# v0.01 Created warning message and set preference file.
# v0.1.0 Basic PK encrypt/decrypt implemented (hard-coded files and keys).
# v0.2 Added the encrypt / decrypt mode option

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
# from tkinter import messagebox
# from random import shuffle
# from threading import Thread
import os
import tkRTF
import pickle
import publicKeyCipherASCII
import makePublicPrivateKeys


class App(tk.Tk):
    def __init__(self, title="Sample App", *args, **kwargs):
        super().__init__()
        self.mode = ""
        self.prefs_filename = ".prefs"
        self.prefs = {}
        try:
            self.load_prefs(self.prefs_filename)  # load the preferences file
        except FileNotFoundError:  # If the file doesn't exist we'll create it anyway
            self.prefs["hide_warning"] = False

        if not self.prefs['hide_warning']:
            self.show_warning_message()
        self.title(title)
        self.setup_frames()
        self.frame_content()

    def setup_frames(self):
        # Create the top (input) frame:
        self.input_frame = tk.LabelFrame(self, text="Input Area")
        self.input_frame.grid(row=0, column=0, columnspan=3,
                              padx=5, pady=5, sticky=tk.NSEW)
        self.input_frame.columnconfigure(0, weight=1)
        self.input_frame.rowconfigure(0, weight=1)

        # Create the middle (alphabet) frame:
        self.mode_frame = tk.LabelFrame(self, text="Mode")
        self.mode_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.mode_frame.columnconfigure(0, weight=1)
        self.mode_frame.rowconfigure(0, weight=1)
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
        self.output_frame = tk.LabelFrame(self, text="Output Area")
        self.output_frame.grid(row=2, column=0, columnspan=3,
                               padx=5, pady=5, sticky=tk.NSEW)
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)

        # Set min size for top and bottom
        self.rowconfigure([0, 2], minsize=90)
        self.rowconfigure(1, weight=1)  # Row 1 should adjust to window size
        # Column 0 should adjust to window size
        self.columnconfigure(0, weight=1)

    def frame_content(self):
        # Content for the input frame
        tk.Label(self.input_frame,
                 text="Please type, paste, or load from file, the input text into this box:").grid(row=0, columnspan=3,
                                                                                                   sticky=tk.W)
        self.input_box = scrolledtext.ScrolledText(
            self.input_frame, height=8, wrap=tk.WORD)
        self.input_box.columnconfigure(0, weight=1)
        self.input_box.grid(row=1, column=0, columnspan=7, sticky=tk.NSEW)
        ttk.Button(self.input_frame,
                   text="Load from File",
                   command=self.fileDialog).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Button(self.input_frame,
                   text="Clear Input",
                   command=self.clear_input).grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Button(self.input_frame,
                   text="Encrypt/Decrypt",
                   command=self.enc_dec).grid(row=2, column=2, padx=5, pady=5, sticky=tk.E)
        # ttk.Button(self.input_frame,
        #            text="Auto Decrypt",
        #            command=self.create_auto_decrypt_window).grid(row=2, column=4, padx=5, pady=5, sticky=tk.E)

        # Content for the Mode Frame:
        self.radio_mode = tk.StringVar()
        self.radio_mode.set("auto")
        tk.Radiobutton(self.mode_frame, text="Encrypt", variable=self.radio_mode,
                       command=self.enc_or_dec, value="encrypt").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Radiobutton(self.mode_frame, text="Decrypt", variable=self.radio_mode,
                       command=self.enc_or_dec, value="decrypt").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Radiobutton(self.mode_frame, text="Auto Detect", variable=self.radio_mode,
                       command=self.enc_or_dec, value="auto").grid(row=2, column=0, padx=5, pady=5,
                                                                   sticky=tk.W)

        # # Content for the analysis tools frame
        # ttk.Button(self.analysis_tools_frame,
        #            text="Index of Coincidence",
        #            command=self.create_ic_window).grid(row=0, column=0, padx=2, pady=2, sticky=tk.NW)
        # ttk.Button(self.analysis_tools_frame,
        #            text="Frequency Analysis",
        #            command=self.create_freq_analysis_window).grid(row=1, column=0, padx=2, pady=2, sticky=tk.NW)
        # ttk.Button(self.analysis_tools_frame,
        #            text="Doubles Analysis",
        #            command=self.create_double_letters_window).grid(row=2, column=0, padx=2, pady=2, sticky=tk.NW)

        # # Content for the key tools frame
        # ttk.Button(self.key_tools_frame,
        #            text="Random Key",
        #            command=self.random_alphabet).grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
        # ttk.Button(self.key_tools_frame,
        #            text="Copy Key to Clipboard",
        #            command=self.copy_key_to_clipboard).grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
        # ttk.Button(self.key_tools_frame,
        #            text="Import Key",
        #            command=self.create_key_import_window).grid(row=2, column=0, padx=2, pady=2, sticky=tk.W)
        # ttk.Button(self.key_tools_frame,
        #            text="Invert Key",
        #            command=self.inv_key).grid(row=3, column=0, padx=2, pady=2, sticky=tk.W)
        # ttk.Button(self.key_tools_frame,
        #            text="Reset Key",
        #            command=self.make_blank_alphabet).grid(row=4, column=0, padx=2, pady=2, sticky=tk.W)

        # Content for the output frame, (one text box only).
        self.output_box = scrolledtext.ScrolledText(
            self.output_frame, width=40, height=8, wrap=tk.WORD)
        self.output_box.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)
        ttk.Button(self.output_frame,
                   text="Copy to Clipboard",
                   command=self.copy_output_to_clipboard).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        # self.create_alphabet_entry_boxes()
        # self.make_blank_alphabet()

    def save_prefs(self, filename):
        with open(filename, 'wb') as handle:
            pickle.dump(self.prefs, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_prefs(self, filename):
        with open(filename, 'rb') as handle:
            self.prefs = pickle.load(handle)

    def pub_key_warning_close(self):
        print("Hide Warning is set to:", self.hide_warning.get())
        self.prefs["hide_warning"] = self.hide_warning.get()
        self.save_prefs(self.prefs_filename)
        self.pub_key_warning_window.destroy()

    def enc_or_dec(self):
        self.mode = self.radio_mode.get()
        if self.radio_mode.get() == "auto":
            self.radio_mode.set("encrypt")
            self.auto_detect_mode()

    def auto_detect_mode(self):
        # Automatically determine whether to encrypt or decrypt based
        # on what's in the input box.
        # If it's largely alphabetic characters - Encrypt
        # Encrypted messages have the message length, blocksize and the
        # encrypted message itself (which is all numeric) separated by
        # the "_" symbol at the start of the text.
        message = self.input_box.get(0.0, tk.END)
        message = message.strip()
        message_part1 = message[:10]
        message_part2 = message[11:500]
        if any(x.isalpha() for x in message):  # If there are alphabetic characters Encrypt
            self.radio_mode.set("encrypt")
        elif "_" in message_part1 and message_part2.isdigit():
            self.radio_mode.set("decrypt")
        else:
            self.radio_mode.set("encrypt")  # If in doubt - set to encrypt

    def enc_dec(self):
        filename = 'output.txt'
        message = self.input_box.get(0.0, tk.END)
        if self.mode == 'encrypt':
            pubkeyFilename = 'PublicKey/m_sansome_pubkey.txt'
            encrypedText = publicKeyCipherASCII.encryptAndWriteToFile(filename, pubkeyFilename,
                                                                      message)
            self.output_box.delete(0.0, tk.END)
            self.output_box.insert(0.0, encrypedText)
        elif self.mode == 'decrypt':
            privKeyFilename = 'PublicKey/m_sansome_privkey.txt'
            decryptedText = publicKeyCipherASCII.messageDecrypt(
                message, privKeyFilename)
            self.output_box.delete(0.0, tk.END)
            self.output_box.insert(0.0, decryptedText)

    def clear_input(self):
        self.input_box.delete(0.0, tk.END)
        self.radio_mode.set('auto')

    def fileDialog(self):
        # Method which invokes the import file dialogue
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select A File", filetypes=[
            ("TXT", "*.txt"),
            ("All files", "*")])
        with open(self.filename) as input_file:
            self.input_box.delete(0.0, tk.END)
            self.input_box.insert(0.0, input_file.read())
        self.auto_detect_mode()

    def copy_to_clipboard(self, output):
        # Main Copy to clipboard method (takes the desired item as a parameter)
        self.clipboard_clear()
        self.clipboard_append(output)
        self.update()  # now it stays on the clipboard after the window is closed

    def copy_output_to_clipboard(self):
        # Copy the output to the clipboard
        out_txt = self.output_box.get(0.0, tk.END)
        self.copy_to_clipboard(out_txt)

    def show_warning_message(self):
        self.pub_key_warning_window = tk.Toplevel(self)
        self.pub_key_warning_window.title("Warning!")
        self.pub_key_warning_window.attributes("-topmost", True)
        self.warning_frame = tk.LabelFrame(
            self.pub_key_warning_window, text="Using this Public Key Encryption / Decryption Tool",
            padx=5, pady=5)
        self.warning_frame.pack(fill="both", expand=True, padx=5, pady=5)

        warn = tkRTF.RichText(self.warning_frame, padx=10, pady=10)

        warn.insert("end", "Important!\n", "h1")
        warn.insert("end", "\nPlease note:\n", "h2")

        warning_text = ("This is what's known as a \"textbook\" implementation "
                        "of the RSA algorithm. Whilst it correctly implements the basics of "
                        "the algorithm, and it will be impervious to the sort of cryptanalitic "
                        "attacks of a normal individual, it will not however resist the attack "
                        "of a professional cryptanalyst or someone who has access to the resources "
                        "of a state or military organisation.")

        warn.insert("end", warning_text, "body_text")
        warn.insert("end", "\n\nUnder no circumstances should this tool be used as anything "
                    "but a learning tool. Do NOT use it in a real environment!\n", "bold")
        warn.pack(fill="both", expand=True)
        self.hide_warning = tk.BooleanVar()

        tk.Checkbutton(self.warning_frame, text="Do not show this message again",
                       variable=self.hide_warning, onvalue=1, offvalue=0).pack(side=tk.LEFT,
                                                                               padx=5, pady=5)

        # warn_close_button = ttk.Button(self.warning_frame, text="Close",
        #                                command=lambda: self.pub_key_warning_window.destroy())
        warn_close_button = ttk.Button(self.warning_frame, text="Close",
                                       command=self.pub_key_warning_close)
        warn_close_button.pack(side=tk.RIGHT)


if __name__ == "__main__":
    App("RSA Public Key Encryption / Decryption Tool").mainloop()
