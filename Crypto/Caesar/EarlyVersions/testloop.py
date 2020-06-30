from tkinter import *

root = Tk()
entList = []

def deleteChar(event):
    event.widget.delete(0, 'end')
    event.widget.insert(0, '')
    event.widget.config(fg='black')

for x in range(12):
    ent = Entry(root, fg='grey60')
    ent.insert(0, 'Enter Name')
    ent.pack()
    ent.bind('<FocusIn>', deleteChar)
    entList.append(ent)
    root.mainloop()