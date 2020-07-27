import tkinter as tk
from tkinter import font as tkFont


class RichText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_font = tkFont.nametofont(self.cget("font"))

        em = default_font.measure("m")
        default_size = default_font.cget("size")
        bold_font = tkFont.Font(**default_font.configure())
        italic_font = tkFont.Font(**default_font.configure())
        h1_font = tkFont.Font(**default_font.configure())
        h2_font = tkFont.Font(**default_font.configure())
        body_text = tkFont.Font(**default_font.configure())

        bold_font.configure(weight="bold")
        italic_font.configure(slant="italic")
        h1_font.configure(size=int(default_size * 2), weight="bold")
        h2_font.configure(size=int(default_size * 1.5), weight="bold")

        self.tag_configure("body_text", wrap="word")
        self.tag_configure("bold", font=bold_font, wrap="word")
        self.tag_configure("italic", font=italic_font, wrap="word")
        self.tag_configure("h1", font=h1_font, spacing3=default_size)
        self.tag_configure("h2", font=h2_font, spacing3=default_size)

        lmargin2 = em + default_font.measure("\u2022 ")
        self.tag_configure("bullet", lmargin1=em, lmargin2=lmargin2)

    def insert_bullet(self, index, text):
        self.insert(index, f"\u2022 {text}", "bullet")


if __name__ == "__main__":
    root = tk.Tk()
    text = RichText(root, width=60, height=30)
    text.pack(fill="both", expand=True)

    text.insert("end", "Rich Text Example\n", "h1")
    text.insert("end", "Hello, world\n\n")
    text.insert_bullet("end", "Item 1\n")
    text.insert_bullet("end", "Item 2\n")

    text.insert("end", "\n")
    text.insert("end", "This line is bold\n", "bold")
    text.insert("end", "This line is italicized\n", "italic")
    text.insert("end", "\nImportant!\n", "h1")
    text.insert("end", "\nPlease note:\n", "h2")

    warning_text = ("This is what's known as a \"textbook\" implementation "
                    "of the RSA algorithm. Whilst it correctly implements the basics of "
                    "the algorithm, and it will be impervious to the sort of cryptanalitic "
                    "attacks of a normal individual, it will not however resist the attack "
                    "of a professional cryptanalyst or someone who has access to the resources "
                    "of a state or military organisation.")

    text.insert("end", warning_text, "body_text")
    text.insert("end", "\n\nUnder no circumstances should this tool be used as anything "
                "but a learning tool. Do NOT use it in a real environment!\n", "bold")

    root.mainloop()
