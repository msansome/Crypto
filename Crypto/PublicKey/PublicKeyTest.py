# A GUI wrapper around the Cracking Codes Book
# - https://www.nostarch.com/crackingcodes/ (BSD Licensed)
#  Public Key Encryption / Decryption program.
# Note: the uses a "textbook" implementation of the RSA algorithm which
# is effective, but not safe against a professional cryptanalitic attack.
# (see the warning message)

# Public Key Encryption / Decryption.

# M. Sansome July 2020
# Version 0.3

# Version History
# ===============
# v0.0 Just the outline structure
# v0.01 Created warning message and set preference file.
# v0.1.0 Basic PK encrypt/decrypt implemented (hard-coded files and keys).
# v0.2 Added the encrypt / decrypt mode option
# v0.3 Completed basic key management functionality

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
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
            self.show_warning_message_window()
        self.priv_key_identifier = '_privkey.txt'
        self.pub_key_identifier = '_pubkey.txt'
        self.key_dir = 'PublicKey/'
        self.pub_key_name = 'm_sansome'
        self.priv_key_name = "m_sansome"
        self.pub_key = self.pub_key_name + self.pub_key_identifier
        self.priv_key = self.priv_key_name + self.priv_key_identifier
        self.pub_keys = self.get_keys(self.pub_key_identifier, self.key_dir)
        self.priv_keys = self.get_keys(self.priv_key_identifier, self.key_dir)
        self.title(title)
        self.setup_frames()
        self.frame_content()
        self.pub_key_select()

    def setup_frames(self):
        # Create the top (input) frame:
        self.input_frame = tk.LabelFrame(self, text="Input Area")
        self.input_frame.grid(row=0, column=0, columnspan=4,
                              padx=5, pady=5, sticky=tk.NSEW)
        self.input_frame.columnconfigure(0, weight=1)
        self.input_frame.rowconfigure(0, weight=1)

        # Create the middle (Mode) frame:
        self.mode_frame = tk.LabelFrame(self, text="Mode")
        self.mode_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.mode_frame.rowconfigure(0, weight=1)
        self.mode_frame.columnconfigure(0, weight=1)

        # Create the middle (Public Key Selection) frame:
        self.pub_key_selection_frame = tk.LabelFrame(self, text="Public Key")
        self.pub_key_selection_frame.grid(
            row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.pub_key_selection_frame.columnconfigure(0, weight=1)
        self.pub_key_selection_frame.rowconfigure(0, weight=1)

        # Create the middle (Private Key Selection) frame:
        self.priv_key_selection_frame = tk.LabelFrame(self, text="Private Key")
        self.priv_key_selection_frame.grid(
            row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.priv_key_selection_frame.columnconfigure(0, weight=1)
        self.priv_key_selection_frame.rowconfigure(0, weight=1)

        # Create the middle (New Key Pair) frame:
        self.new_key_pair_frame = tk.LabelFrame(self, text="New Key Pair")
        self.new_key_pair_frame.grid(
            row=1, column=3, padx=5, pady=5, sticky=tk.E)
        self.new_key_pair_frame.columnconfigure(0, weight=1)
        self.new_key_pair_frame.rowconfigure(0, weight=1)

        # Create the bottom (output) frame:
        self.output_frame = tk.LabelFrame(self, text="Output Area")
        self.output_frame.grid(row=2, column=0, columnspan=4,
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
            self.input_frame, height=12, wrap=tk.WORD)
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

        # Content for the Mode Frame:
        self.radio_mode = tk.StringVar()
        self.radio_mode.set("auto")
        ttk.Radiobutton(self.mode_frame, text="Encrypt", variable=self.radio_mode,
                        command=self.enc_or_dec, value="encrypt").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(self.mode_frame, text="Decrypt", variable=self.radio_mode,
                        command=self.enc_or_dec, value="decrypt").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(self.mode_frame, text="Auto Detect", variable=self.radio_mode,
                        command=self.enc_or_dec, value="auto").grid(row=2, column=0, padx=5, pady=5,
                                                                    sticky=tk.W)

        # Content for the Public Keys Frame:
        self.key_choice = tk.StringVar()
        ttk.Label(self.pub_key_selection_frame, text="Please select key to use:",
                  ).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.pub_key_combo = ttk.Combobox(self.pub_key_selection_frame,
                                          textvariable=self.key_choice,
                                          state="readonly", values=self.pub_keys)
        self.pub_key_combo.current(
            self.pub_keys.index(self.pub_key_name))
        self.pub_key_combo.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.pub_key_combo.bind("<<>ComboboxSelected>")

        # Content for the Private Keys Frame:
        self.priv_key_choice = tk.StringVar()
        ttk.Label(self.priv_key_selection_frame, text="Please select key to use:",
                  ).grid(row=0, column=0, pady=5, sticky=tk.W)
        self.priv_key_combo = ttk.Combobox(self.priv_key_selection_frame,
                                           textvariable=self.priv_key_choice, state="readonly",
                                           values=self.priv_keys)
        self.priv_key_combo.current(
            self.priv_keys.index(self.priv_key_name))
        self.priv_key_combo.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.priv_key_combo.bind("<<>ComboboxSelected>")

        # Content for the New Key Pair Frame:
        ttk.Button(self.new_key_pair_frame, text="Create a new Key Pair").grid(
            row=0, column=0, padx=5, pady=5)

        # Content for the output frame, (one text box only).
        self.output_box = scrolledtext.ScrolledText(
            self.output_frame, width=50, height=12, wrap=tk.WORD)
        self.output_box.grid(row=0, column=0,
                             columnspan=3, sticky=tk.NSEW)
        ttk.Button(self.output_frame,
                   text="Copy to Clipboard",
                   command=self.copy_output_to_clipboard).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    def get_keys(self, key_identifier, key_dir):
        strp = len(key_identifier)
        keys = []
        # keys = [file for file in os.listdir(key_dir) if file.endswith('privkey.txt')]
        for file in os.listdir(key_dir):
            if file.endswith(key_identifier):
                keys.append(file[:-strp])
        return keys

    def pub_key_select(self):
        selected = self.pub_key_combo.get()
        self.pub_key = selected + self.pub_key_identifier

    def priv_key_select(self):
        selected = self.priv_key_combo.get()
        self.priv_key = selected + self.priv_key_identifier

    def save_prefs(self, filename):
        with open(filename, 'wb') as handle:
            pickle.dump(self.prefs, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_prefs(self, filename):
        with open(filename, 'rb') as handle:
            self.prefs = pickle.load(handle)

    def enc_or_dec(self):
        self.mode = self.radio_mode.get()
        if self.radio_mode.get() == "auto":
            self.detect_mode()
        self.update_the_combos()

    def detect_mode(self):
        # Automatically determine whether to encrypt or decrypt based
        # on what's in the input box.
        # If it's largely alphabetic characters - Encrypt
        # Encrypted messages have the message length, blocksize and the
        # encrypted message itself (which is all numeric) separated by
        # the "_" symbol at the start of the text.
        self.mode = self.radio_mode.get()
        if self.radio_mode.get() == "auto":
            self.radio_mode.set("encrypt")
            self.mode = "encrypt"
        message = self.input_box.get(0.0, tk.END)
        message = message.strip()
        message_part1 = message[:10]
        message_part2 = message[11:500]
        if any(x.isalpha() for x in message):  # If there are alphabetic characters Encrypt
            self.radio_mode.set("encrypt")
            self.mode = "encrypt"
        elif "_" in message_part1 and message_part2.isdigit():
            self.radio_mode.set("decrypt")
            self.mode = "decrypt"
        else:
            self.radio_mode.set("encrypt")  # If in doubt - set to encrypt
            self.mode = "encrypt"
        self.update_the_combos()

    def enc_dec(self):
        # self.detect_mode()
        self.pub_key_select()
        self.priv_key_select()
        filename = 'output.txt'
        message = self.input_box.get(0.0, tk.END)
        if self.mode == 'encrypt':
            # pubkeyFilename = 'PublicKey/m_sansome_pubkey.txt'
            encrypedText = publicKeyCipherASCII.encryptAndWriteToFile(filename,
                                                                      (self.key_dir + "/" + self.pub_key), message)
            self.output_box.delete(0.0, tk.END)
            self.output_box.insert(0.0, encrypedText)
        elif self.mode == 'decrypt':
            # privKeyFilename = 'PublicKey/m_sansome_privkey.txt'
            try:
                decryptedText = publicKeyCipherASCII.messageDecrypt(
                    message, (self.key_dir + self.priv_key))
                self.output_box.delete(0.0, tk.END)
                self.output_box.insert(0.0, decryptedText)
            except:
                tk.messagebox.showerror(
                    "Error", "Hmmm... Have you used the wrong key?")

    def update_the_combos(self):
        if self.mode == "decrypt":
            self.pub_key_combo.configure(state="disabled")
            self.priv_key_combo.configure(state="readonly")
        if self.mode == "encrypt":
            self.priv_key_combo.configure(state="disabled")
            self.pub_key_combo.configure(state="readonly")

    def clear_input(self):
        self.input_box.delete(0.0, tk.END)
        self.radio_mode.set('auto')

    def fileDialog(self):
        # Method which invokes the import file dialogue
        self.clear_input()  # Empty the input box first
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select A File", filetypes=[
            ("TXT", "*.txt"),
            ("All files", "*")])
        try:
            with open(self.filename) as input_file:
                self.input_box.delete(0.0, tk.END)
                self.input_box.insert(0.0, input_file.read())
        except (FileNotFoundError, TypeError):  # If you hit "cancel" you get an error
            pass
        self.detect_mode()  # Once loaded - detect what type of file it is.

    def copy_to_clipboard(self, output):
        # Main Copy to clipboard method (takes the desired item as a parameter)
        self.clipboard_clear()
        self.clipboard_append(output)
        self.update()  # now it stays on the clipboard after the window is closed

    def copy_output_to_clipboard(self):
        # Copy the output to the clipboard
        out_txt = self.output_box.get(0.0, tk.END)
        self.copy_to_clipboard(out_txt)

    def show_warning_message_window(self):
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
                                       command=self.close_warning_message_window)
        warn_close_button.pack(side=tk.RIGHT)

    def close_warning_message_window(self):
        print("Hide Warning is set to:", self.hide_warning.get())
        self.prefs["hide_warning"] = self.hide_warning.get()
        self.save_prefs(self.prefs_filename)
        self.pub_key_warning_window.destroy()


if __name__ == "__main__":
    App("RSA Public Key Encryption / Decryption Tool").mainloop()
