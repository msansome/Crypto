from tkinter import font as tkfont


class Headline(object):
  def __init__(self, x, y, canvas, text):
    self.font = tkfont.Font(family="Helvetica", size=20,
                            weight="bold", underline=1)
    # https://www.tutorialspoint.com/python/tk_fonts.htm
    canvas.create_text(x, y, text=text, anchor='nw',
                       font=self.font, fill='black',
                       activefill='green')


class Heading1(object):
  def __init__(self, x, y, canvas, text):
    self.font = tkfont.Font(family="Helvetica", size=20,
                            weight="bold")
    canvas.create_text(x, y, text=text, anchor='nw',
                       font=self.font, fill='black',
                       activefill='green')


class Heading2(object):
  def __init__(self, x, y, canvas, text):
    self.font = tkfont.Font(family="Helvetica", size=18,
                            weight="bold")
    canvas.create_text(x, y, text=text, anchor='nw',
                       font=self.font, fill='black',
                       activefill='green')


class BodyText(object):
  def __init__(self, x, y, canvas, text):
    self.font = tkfont.Font(family="Helvetica", size=12)
    canvas.create_text(x, y, text=text, anchor='nw',
                       font=self.font, fill='black', width=480,
                       activefill='green')


class BodyBold(object):
  def __init__(self, x, y, canvas, text):
    self.font = tkfont.Font(family="Helvetica", size=12, weight="bold")
    canvas.create_text(x, y, text=text, anchor='nw',
                       font=self.font, fill='black', width=480,
                       activefill='green')
