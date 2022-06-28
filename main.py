import tkinter as tk
import random
import time
import threading
from os import abort
from english_words import english_words_lower_set


class Interface:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Speed Typing Test')
        self.root.attributes('-fullscreen', True)
        self.root.config(bg="#CDAA7D")
        self.root.bind("<Escape>", lambda event: abort())
        self.root.bind("<Return>", self.insert)
        self.frame = tk.Frame(self.root)
        self.frame.config(bg="#CDAA7D")
        self.samples = random.sample(list(english_words_lower_set), 5)
        self.samples.append('typing finished!')

        self.title = tk.Label(self.frame, 
                            text="Type as fast as you can!", 
                            font=("Gill Sans Ultra Bold", 25),
                            bg="#CDAA7D",
                            fg="#8B1A1A")
        self.title.grid(row=0, column=0, columnspan=2, padx=5, pady=70)

        self.label = tk.Label(self.frame, 
                            text=self.samples[0].title(), 
                            font=("Gill Sans Ultra Bold", 25),
                            bg="#CDAA7D")
        self.label.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        self.speed = tk.Label(self.frame, 
                            text='0.00 seconds', 
                            font=("Gill Sans Ultra Bold", 20),
                            bg="#CDAA7D")
        self.speed.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.input = tk.Entry(self.frame, width=40, font=("Gill Sans Ultra Bold", 20))
        self.input.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        self.input.bind("<KeyPress>", self.start)
        self.input.focus_set()

        self.reset = tk.Button(self.frame,
                            text='Reset', 
                            command=self.reset,
                            bg="#9C9C9C",
                            padx=100,
                            pady=25,
                            font=("Gill Sans Ultra Bold", 15),
                            activebackground='#345',
                            activeforeground='white',
                            borderwidth=3,
                            relief='raised',
                            )
        self.reset.grid(row=4, column=0, columnspan=1, padx=5, pady=10)

        self.quit = tk.Button(self.frame,
                            text='Quit', 
                            command=self.quit,
                            bg="#9C9C9C",
                            padx=100,
                            pady=25,
                            font=("Gill Sans Ultra Bold", 15),
                            activebackground='#345',
                            activeforeground='white',
                            borderwidth=3,
                            relief='raised',
                            )
        self.quit.grid(row=4, column=1, columnspan=1, padx=5, pady=10)

        self.frame.pack(expand=True)
        self.running = False
        self.scores = [0, 0]
        self.root.mainloop()

    def start(self, event):
        if not self.running:
            if self.label.cget('text') == 'Typing Finished!':
                pass
            elif not event.keycode in [16, 17, 18]: #Shift, Alt, Control
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()
        if not self.label.cget('text').startswith(self.input.get()):
            self.input.config(fg="red")
        else:
            self.input.config(fg="black")

    def insert(self, event):
        if self.input.get() == self.label.cget('text'):
            self.scores[0] += 1
            self.samples.remove(self.label.cget('text').lower())
        else:
            self.scores[1] += 1
            self.samples.remove(self.label.cget('text').lower())
        self.input.delete(0, tk.END)    
        self.label.config(text=self.samples[0].title())
        if self.label.cget('text') == 'Typing Finished!':
            self.running = False
            self.input.config(state='disabled')
            self.report_insertion

    def time_thread(self):
        initial_time = time.time()
        while self.running:
            clock = time.time()
            self.speed.config(text=f'{clock - initial_time:.2f} seconds')

    def reset(self):
        self.running = False
        self.speed.config(text='0.00 seconds')
        self.samples = random.sample(list(english_words_lower_set), 5)
        self.samples.append(' ')
        self.label.config(text=random.choice(self.samples).title())
        self.input.delete(0, tk.END)

    def quit(self):
        self.root.destroy()
        abort()


if __name__ == '__main__':
    Interface()