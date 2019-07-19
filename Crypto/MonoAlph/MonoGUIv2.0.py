"""Refactored version of the GUI Substition Cipher Tool
M Sansome
June 2019"""

##from datetime import datetime
##import os
##import csv
import tkinter as tk
from tkinter import ttk


class LabelInput(tk.Frame):
    """A widget containing a label and input together"""

    def __init__(self, parent, label = "", input_class=ttk.Entry, input_var=None, input_args=None, label_args=None, **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var

        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args["text"] = label
            input_args["variable"] = input_var
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky='we')
            input_args["textvariable"] = input_var

        self.input = input_class(self, **input_args)
        self.input.grid(row=1, column=0, sticky='we')
        self.columnconfigure(0,weight=1)

    def grid(self, sticky='we', **kwargs):
        super().grid(sticky=sticky, **kwargs)

    def get(self):
        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input) == tk.Text:
                return self.input.get('1.0','end')
            else:
                return self.input.get()
        except (TypeError, tk.TclError):
            # happens when numeric fields are empty.
            return ''

    def set(self, value, *args, **kwargs):
        if type(self.variable) == tk.BooleanVar:
            self.variable.set = (bool(value))
        elif self.variable:
            self.variable.set(value, *args, **kwargs)
        elif type(self.input) in (ttk.Checkbutton, ttk.Radiobutton):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:
            self.input.delete('1.0', 'end')
            self.input.insert('1.0', value)
        else: # input must be an Entry-type widget with no variable
            self.input.delete(0, 'end')
            self.input.insert(0, value)
            
                              
class SubstitutionForm(tk.Frame):
    """The input form for our widgets"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # A dict to keep track of input widgets
        self.inputs = {}

        
        ciphertextArea = tk.LabelFrame(self, text="Type or Paste the Ciphertext here:")

        self.scrollbar1 = ttk.Scrollbar(ciphertextArea)
        
        self.inputs['Ciphertext'] = LabelInput(ciphertextArea, "Ciphertext", input_class=tk.Text, input_args={"width":75, "height": 10})
        self.inputs['Ciphertext'].grid(sticky='w', row=0, column=0, padx=10)
        #self.inputs['Ciphertext'].grid(row=0, column=0)
        self.inputs[ciphertext_entry] = LabelInput(ciphertextArea, "CiphertextEntry", input_class=tk.Text, input_args={'wrap = word', 'yscrollcommand=ciphertextArea.scrollbar1.set', 'height=5'})
        #self.text_entry_box = tk.Text(master, wrap='word', yscrollcommand=self.scrollbar1.set, height=5)

        self.inputs['Ciphertext'].scrollbar1.config(command=ciphertextArea.ciphertext_entry.yview)
        #self.scrollbar2.config(command=self.text_output_box.yview)
        self.scrollbar1.grid(column=0, row=1,  sticky='nsw')
        #self.scrollbar2.grid(column=27, row=12,  sticky='nsw')



       
##        self.inputs['Date'] = LabelInput(ciphertextArea, "Date", input_var=tk.StringVar())
##        self.inputs['Date'].grid(row=0, column=0)
##
##        self.inputs['Time'] = LabelInput(ciphertextArea, "Time", input_class=ttk.Combobox, input_var=tk.StringVar(), input_args={"values": ["08:00","12:00","16:00","20:00"]})
##        self.inputs['Time'].grid(row=0, column=1)
##
##        self.inputs['Technician'] = LabelInput(ciphertextArea, "Technician", input_var=tk.StringVar())
##        self.inputs['Technician'].grid(row=0, column=2)
##
##        # Line 2
##        self.inputs['Lab'] = LabelInput(ciphertextArea, "Lab", input_class=ttk.Combobox, input_var=tk.StringVar(), input_args={"values": ["A","B","C","D","E"]})
##        self.inputs['Lab'].grid(row=1, column=0)
##
##        self.inputs['Plot'] = LabelInput(ciphertextArea, "Plot", input_class=ttk.Combobox, input_var=tk.IntVar(), input_args={"values": list(range(1,21))})
##        self.inputs['Plot'].grid(row=1, column=1)
##
##        self.inputs['Seed sample'] = LabelInput(ciphertextArea, "Seed sample", input_var=tk.StringVar())
##        self.inputs['Seed sample'].grid(row=1, column=2)

        ciphertextArea.grid(row=0, column=0, sticky='we')

        # Environment Data
        environmentinfo = tk.LabelFrame(self, text="Envirnment Data")

        self.inputs['Humidity'] = LabelInput(environmentinfo, "Humidity (g/m³)", input_class=tk.Spinbox, input_var=tk.DoubleVar(), input_args={"from_": 0.5, "to": 52.0, "increment": .01})
        self.inputs['Humidity'].grid(row=0, column=0)

        self.inputs['Light'] = LabelInput(environmentinfo, "Light (klx)", input_class=tk.Spinbox, input_var=tk.DoubleVar(), input_args={"from_": 0, "to": 100, "increment": .01})
        self.inputs['Light'].grid(row=0, column=1)

        self.inputs['Temperature'] = LabelInput(environmentinfo, "Temperature (°C)", input_class=tk.Spinbox, input_var=tk.DoubleVar(), input_args={"from_": 4, "to": 40, "increment": .01})
        self.inputs['Temperature'].grid(row=0, column=2)

        self.inputs['Equipment Fault'] = LabelInput(environmentinfo, "Equipment Fault", input_class=ttk.Checkbutton, input_var=tk.BooleanVar())
        self.inputs['Equipment Fault'].grid(row=1, column=0, columnspan=3)

        environmentinfo.grid(row=1, column=0, sticky='we')
                                         
        # Plant Info
        plantinfo = tk.LabelFrame(self, text="Plant Data")

        self.inputs['Plants'] = LabelInput(plantinfo, "Plants", input_class=tk.Spinbox, input_var=tk.IntVar(), input_args={"from_": 0, "to": 20})
        self.inputs['Plants'].grid(row=0, column=0)

        self.inputs['Blossoms'] = LabelInput(plantinfo, "Blossoms", input_class=tk.Spinbox, input_var=tk.IntVar(), input_args={"from_": 0, "to": 1000})
        self.inputs['Blossoms'].grid(row=0, column=1)

        self.inputs['Fruit'] = LabelInput(plantinfo, "Fruit", input_class=tk.Spinbox, input_var=tk.IntVar(), input_args={"from_": 0, "to": 1000})
        self.inputs['Fruit'].grid(row=0, column=2)

        self.inputs['Min Height'] = LabelInput(plantinfo, "Min Height", input_class=tk.Spinbox, input_var=tk.IntVar(), input_args={"from_": 0, "to": 1000})
        self.inputs['Min Height'].grid(row=1, column=0)

        self.inputs['Max Height'] = LabelInput(plantinfo, "Max Height", input_class=tk.Spinbox, input_var=tk.IntVar(), input_args={"from_": 0, "to": 1000})
        self.inputs['Max Height'].grid(row=1, column=1)

        self.inputs['Median Height'] = LabelInput(plantinfo, "Median Height", input_class=tk.Spinbox, input_var=tk.IntVar(), input_args={"from_": 0, "to": 1000})
        self.inputs['Median Height'].grid(row=1, column=2)

        plantinfo.grid(row=2, column=0, sticky='we')

        # Notes Section
        self.inputs['Notes'] = LabelInput(self, "Notes", input_class=tk.Text, input_args={"width":75, "height": 10})
        self.inputs['Notes'].grid(sticky='w', row=3, column=0)

        self.reset()

    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data

    def reset(self):
        for widget in self.inputs.values():
            widget.set('')
        

class Application(tk.Tk):
    """Application root window"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Subtitution Cipher Tool")
        self.resizable(width=False, height=False)

        ttk.Label(self, text="MCS Substition Cipher Tool", font=("tkDefaultFont", 16)).grid(row=0)
        self.recordform = SubstitutionForm(self)
        self.recordform.grid(row=1, padx=10)

        self.savebutton = ttk.Button(self, text="Save", command=self.on_save)
        self.savebutton.grid(sticky='e', row=2, padx=10)

        # Status Bar
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky='we', row=3, padx=10)

        self.records_saved = 0
        

    def on_save(self):
        datestring = datetime.today().strftime("%Y-%m-%d")
        filename = f"mcs_data_record_{datestring}.csv"
        newfile = not os.path.exists(filename)

        data = self.recordform.get()

        with open(filename, 'a') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)

        self.records_saved += 1
        self.status.set(f"{self.records_saved} records saved this session.")

        self.recordform.reset()
            
        
        

if __name__ == "__main__":
    app = Application()
    app.mainloop()

    
