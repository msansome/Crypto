# A simple GUI application for brute force
# decryption of a Caesar Cipher

# Mark Sansome June 2020


from tkinter import *
from tkinter import scrolledtext
from Caesar.CaesarTextV2_0 import caesar # Import the decryption module from my text based version


class Application(Frame):
    """ Some text here."""
    def __init__(self,master):
        """Initialise the Frame"""
        super(Application, self).__init__(master)

        self.ciphertext = ""
        self.shortText = ""

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.grid()

        self.input_frame = LabelFrame(self, text = "Ciphertext", padx=5, pady=5)
        self.input_frame.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10, sticky=NSEW)
        self.key_selection_frame = LabelFrame(self, text="Select which Key to use for decryption")
        self.key_selection_frame.grid(row=1, column=0, columnspan = 3, padx = 10, pady = 10, sticky=NSEW)
        self.output_frame = LabelFrame(self, text="Plaintext")
        self.output_frame.grid(row=2, column=0, columnspan = 3, padx = 10, pady = 10, sticky=NSEW)

        self.input_frame.rowconfigure(0, weight=1)
        self.input_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)
        self.output_frame.columnconfigure(0, weight=1)


        self.create_widgets()

    def create_widgets(self):
        """Create widgets."""
        self.key = IntVar() # Variable used to hold decryption key

        # create an input box
        Label(self.input_frame,
              text="Please type, or paste, the text to be decrypted into this box:").grid(row=0, sticky=W)
        self.input_box = scrolledtext.ScrolledText(self.input_frame, width=40, height=5, wrap=WORD)
        self.input_box.grid(row=1, column=0, columnspan=3, sticky=NSEW)
        Button(self.input_frame,
               text = "Decrypt",
               command = self.draw_choices).grid(row = 2, column = 2, sticky = E)

        # create an output box
        self.output_box = scrolledtext.ScrolledText(self.output_frame, width = 40, height = 5, wrap = WORD)
        self.output_box.grid(row = 0, column = 0, columnspan = 3, sticky=NSEW)

    def draw_choices(self):
        """ This method will display one line per key for 25 keys"""
        self.get_ciphertext()
        for i in range(25):
            Radiobutton(self.key_selection_frame,
                        text=f"Key = {i + 1}: ", variable=self.key,
                        value=i,
                        command=self.doDecrypt
                        ).grid(row=i, column=0, sticky=W)
            Label(self.key_selection_frame,
                  text=caesar(self.shortText, i + 1, True),
                  anchor=W
                  ).grid(row=i, column=1, sticky=W)

    def get_ciphertext(self):
        """ Will get the ciphertext from the input box and also create a shortened version to display on one line"""
        screenWidth = 78
        self.ciphertext = self.input_box.get(0.0, END)

        if len(self.ciphertext) > screenWidth:
            self.shortText = self.ciphertext[:screenWidth]
        else:
            self.shortText = self.ciphertext[:]
        self.shortText = self.shortText.replace('\n', ' ') # strip out carriage returns just in case


    def doDecrypt(self):
        """This will ultimately decrypt and display the results"""
        key = self.key.get() # Get key from radio button press
        output_txt = caesar(self.ciphertext, key + 1, True)
        self.output_box.delete(0.0,END)
        self.output_box.insert(0.0, output_txt)

# main
root = Tk()
root.title("Caesar Cipher - Brute Force Decryption Tool")
#root.geometry("300x150")
app = Application(root)
root.mainloop()