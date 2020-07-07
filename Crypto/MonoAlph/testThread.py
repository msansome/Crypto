
import tkinter as tk
from threading import Thread
from random import randint
import time

class MyTestClass: # This would actually be imported from another module
    def __init__(self):
        self.stopped = False

    def my_long_procedure(self):
        count = 0
        maxscore = 0
        i = 0
        while count < 1000 and not self.stopped:
            i += 1
            score = randint(1,10000)
            if score > maxscore:
                maxscore = score
                self.message = f'This is iteration {i} and the best score is {maxscore}'
                print(self.message)
                # self.carry_on = input("Do you want to continue? ")
                # if self.carry_on.upper() != "Y":
                #     return maxscore
            time.sleep(2)
        print('OK - You stopped me...')

class MyMainApp(tk.Tk):
    def __init__(self, title="Sample App", *args, **kwargs):
        super().__init__()
        self.title(title)
        self.test_run = MyTestClass()
        self.frame1 = tk.LabelFrame(self, text="My Frame")
        self.frame1.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
        self.frame1.columnconfigure(0, weight=1)
        self.frame1.rowconfigure(0, weight=1)

        start_button = tk.Button(self.frame1, text="Start!",
                                command=self.start_proc).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        stop_button = tk.Button(self.frame1, text="Stop!",
                                command=self.stop_proc).grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)
        self.output_box = tk.Text(self.frame1, width=60, height=8, wrap=tk.WORD)
        self.output_box.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)

    def start_proc(self):
        self.test_run.stopped = False
        self.control_thread = Thread(target=self.test_run.my_long_procedure, daemon=True)
        self.control_thread.start()
        time.sleep(1)
        self.output_box.delete(0.0, tk.END)
        self.output_box.insert(0.0, self.test_run.message)
        # self.control_thread.join()
        # while not self.test_run.stopped:
        #     self.output_box.delete(0.0, tk.END)
        #     self.output_box.insert(0.0, self.test_run.message)
        #     time.sleep(0.5)

    def stop_proc(self):
        self.test_run.stopped = True

if __name__ == "__main__":
    MyMainApp("My Test App").mainloop()
