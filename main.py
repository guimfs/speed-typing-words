import tkinter as tk
import random
import time
import threading
from os import abort
from english_words import english_words_lower_set
from pymongo import MongoClient


class Interface:

    def __init__(self):
        """This method is the constructor for frames, labels, buttons and entries"""
        # Creating the root
        self.root = tk.Tk()
        self.root.title('Speed Typing Test')
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda event: abort())
        self.root.bind("<Return>", self.insert)
        self.root.config(bg="#CDAA7D")
        
        # Miscellaneous variables
        self.samples = random.sample(list(english_words_lower_set), 5)
        self.samples.append('typing finished!')
        self.scores = [0, 0]

        # Creating frames
        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)
        self.frame3 = tk.Frame(self.root)

        for frame in (self.frame1, self.frame2, self.frame3):
            pass

        # Creating the frame1 (game)
        self.frame1 = tk.Frame(self.root)
        self.frame1.config(bg="#CDAA7D")
          
        self.title_f1 = tk.Label(self.frame1, 
                            text="Type as fast as you can!", 
                            font=("Gill Sans Ultra Bold", 25),
                            bg="#CDAA7D",
                            fg="#8B1A1A")
        self.title_f1.grid(row=0, column=0, columnspan=2, padx=5, pady=70)

        self.label_f1 = tk.Label(self.frame1, 
                            text=self.samples[0].title(), 
                            font=("Gill Sans Ultra Bold", 25),
                            bg="#CDAA7D")
        self.label_f1.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        self.speed_f1 = tk.Label(self.frame1, 
                            text='0.00 seconds', 
                            font=("Gill Sans Ultra Bold", 20),
                            bg="#CDAA7D")
        self.speed_f1.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.input_f1 = tk.Entry(self.frame1, width=40, font=("Gill Sans Ultra Bold", 20))
        self.input_f1.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        self.input_f1.bind("<KeyPress>", self.start)
        self.input_f1.focus_set()

        self.reset_f1 = tk.Button(self.frame1,
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
        self.reset_f1.grid(row=4, column=0, columnspan=1, padx=5, pady=10)

        self.quit_f1 = tk.Button(self.frame1,
                            text='Menu', 
                            command=self.change_to_menu_from_game,
                            bg="#9C9C9C",
                            padx=100,
                            pady=25,
                            font=("Gill Sans Ultra Bold", 15),
                            activebackground='#345',
                            activeforeground='white',
                            borderwidth=3,
                            relief='raised',
                            )
        self.quit_f1.grid(row=4, column=1, columnspan=1, padx=5, pady=10)

        # Creating frame2 (menu)
        self.frame2 = tk.Frame(self.root)
        self.frame2.config(bg="#CDAA7D", )
          
        self.title_f2 = tk.Label(self.frame2, 
                            text="Menu", 
                            font=("Gill Sans Ultra Bold", 25),
                            bg="#CDAA7D",
                            fg="#8B1A1A")
        self.title_f2.grid(row=0, column=0, columnspan=2, padx=5, pady=70)

        self.label_f2 = tk.Label(self.frame2, 
                            text=self.samples[0].title(), 
                            font=("Gill Sans Ultra Bold", 25),
                            bg="#CDAA7D")
        self.label_f2.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        self.speed_f2 = tk.Label(self.frame2, 
                            text='0.00 seconds', 
                            font=("Gill Sans Ultra Bold", 20),
                            bg="#CDAA7D")
        self.speed_f2.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.input_f2 = tk.Entry(self.frame2, width=40, font=("Gill Sans Ultra Bold", 20))
        self.input_f2.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        self.input_f2.bind("<KeyPress>", self.start)
        self.input_f2.focus_set()

        self.reset_f2 = tk.Button(self.frame2,
                            text='Play', 
                            command=self.change_to_game_from_menu,
                            bg="#9C9C9C",
                            padx=100,
                            pady=25,
                            font=("Gill Sans Ultra Bold", 15),
                            activebackground='#345',
                            activeforeground='white',
                            borderwidth=3,
                            relief='raised',
                            )
        self.reset_f2.grid(row=4, column=0, columnspan=1, padx=5, pady=10)

        self.quit_f2 = tk.Button(self.frame2,
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
        self.quit_f2.grid(row=4, column=1, columnspan=1, padx=5, pady=10)
        self.frame2.pack(expand=True)

        # Creating frame3 (scores database)

        # Creating frame4 (final score)

        # Miscellaneous variables
        self.name = 'Still need to insert this variable'
        self.running = False

        # Raise
        self.show_frame(self.frame2)

        # Looping the root
        self.root.mainloop()

    def start(self, event):
        """This method will run when any key is pressed (except Shift, Alt and Control)"""
        if not self.running:
            if self.label_f1.cget('text') == 'Typing Finished!':
                pass
            elif not event.keycode in [16, 17, 18]: # Shift, Alt, Control
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()
        if not self.label_f1.cget('text').startswith(self.input_f1.get()):
            self.input_f1.config(fg="red")
        else:
            self.input_f1.config(fg="black")

    def insert(self, event):
        """
        This method will run after each word entered and count positive or negative score.
        After count all the words typed, it will insert in MongoDB database.   
        """
        if self.input_f1.get() == self.label_f1.cget('text'):
            self.scores[0] += 1
            self.samples.remove(self.label_f1.cget('text').lower())
        else:
            self.scores[1] += 1
            self.samples.remove(self.label_f1.cget('text').lower())
        self.input_f1.delete(0, tk.END)    
        self.label_f1.config(text=self.samples[0].title())
        if self.label_f1.cget('text') == 'Typing Finished!':
            self.running = False
            self.input_f1.config(state='disabled')
            self.insert_database()
            self.scores.clear()
            self.scores = [0, 0]

    def time_thread(self):
        """This is a threading method that will run timer"""
        initial_time = time.time()
        while self.running:
            clock = time.time()
            self.speed_f1.config(text=f'{clock - initial_time:.2f} seconds')

    def reset(self):
        """This method will reset the objects"""
        self.running = False
        time.sleep(0.1)
        self.speed_f1.config(text='0.00 seconds')
        self.samples = random.sample(list(english_words_lower_set), 5)
        self.samples.append('typing finished!')
        self.label_f1.config(text=self.samples[0].title())
        self.input_f1.delete(0, tk.END)

    def quit(self):
        """This method will run when quit button is pressed"""
        self.root.destroy()
        abort()

    def show_frame(self, frame):
        """This method will help the frame changing between menu, game, scores database and final score"""
        frame.tkraise()

    def change_to_menu_from_game(self):
        """This method will change to menu screen from game screen"""
        self.frame2.pack(expand = True)
        self.frame1.forget()

    def change_to_game_from_menu(self):
        """This method will change to game screen from menu screen"""
        self.frame1.pack(expand = True)
        self.frame2.forget()

    def insert_database(self):
        """This method will insert a new or update a existent data in a MongoDB database"""
        client = MongoClient('localhost', 27017)
        database = client['speed-typing']
        data = {
            'name': self.name,
            'score_positive': self.scores[0], 
            'score_negative': self.scores[1]
        }
        records = database['records']
        if records.find_one({'name': data.get('name')}):
            records.update_one({'name': self.name}, {'$set': {'score_positive': self.scores[0], 'score_negative': self.scores[1]}})
        else:
            records.insert_one(data)


if __name__ == '__main__':
    Interface()