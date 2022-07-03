import tkinter as tk
import random
import time
import threading
from os import abort
from xml.dom.expatbuilder import theDOMImplementation
from english_words import english_words_lower_set
from pymongo import MongoClient
from tkinter import CENTER, ttk


class Interface:

    """This will load all datas from MongoDB"""
    client = MongoClient('localhost', 27017)
    database = client['speed-typing']
    records = database['records']
    list_leader = []
    all_records = records.find()
    for item in all_records:
        list_leader.append(
            (
                item.get('name'),
                item.get('mode'),
                item.get('accuracy'),
                item.get('time')
            )
        )

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
        self.dict = {'Easy (5 words)': 5, 'Medium (10 words)': 10, 'Hard (20 words)': 20}
        self.scores = [0, 0]
        self.running = False

        # Creating frame2 (menu)
        self.frame2 = tk.Frame(self.root)
        self.frame2.config(bg="#CDAA7D")
          
        self.title_f2 = tk.Label(self.frame2, 
                            text="Menu", 
                            font=("Gill Sans Ultra Bold", 30),
                            bg="#CDAA7D",
                            fg="#8B1A1A")
        self.title_f2.grid(row=0, column=0, columnspan=3, padx=5, pady=10)

        self.label_f2 = tk.Label(self.frame2, 
                            text='A simple Speed Typing Game to\n practice your typing technique.', 
                            font=("Gill Sans Ultra Bold", 25),
                            bg="#CDAA7D")
        self.label_f2.grid(row=1, column=0, columnspan=3, padx=5, pady=30)

        self.label_name_f2 = tk.Label(self.frame2, 
                            text='Insert your name', 
                            font=("Gill Sans Ultra Bold", 20),
                            bg="#CDAA7D")
        self.label_name_f2.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        self.name_f2 = tk.Entry(self.frame2, justify='center', width=15, font=("Gill Sans Ultra Bold", 19))
        self.name_f2.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
        self.name_f2.focus_set()

        self.label_difficulty_f2 = tk.Label(self.frame2, 
                            text='Select the difficulty', 
                            font=("Gill Sans Ultra Bold", 20),
                            bg="#CDAA7D")
        self.label_difficulty_f2.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        self.current_var = tk.StringVar()
        self.difficulty_f2 = ttk.Combobox(self.frame2,
                            width=15,
                            textvariable=self.current_var,
                            font=("Gill Sans Ultra Bold", 19),
                            values=list(self.dict.keys()),
                            state='readonly',
                            justify='center'
                            )
        self.difficulty_f2.grid(row=5, column=0, columnspan=3, padx=10, pady=5)
        self.difficulty_f2.bind("<<ComboboxSelected>>", lambda event: self.test.config(text=self.current_var.get()))

        self.test = tk.Label(self.frame2, 
                            text='',
                            font=("Gill Sans Ultra Bold", 20),
                            bg="#CDAA7D")
        self.test.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

        self.samples = random.sample(list(english_words_lower_set), 5)
        self.samples.append('typing finished!')

        self.play_f2 = tk.Button(self.frame2,
                            text='Play', 
                            command=self.change_to_game_from_menu,
                            bg="#9C9C9C",
                            padx=70,
                            pady=15,
                            font=("Gill Sans Ultra Bold", 15),
                            activebackground='#345',
                            activeforeground='white',
                            borderwidth=3,
                            relief='raised',
                            )
        self.play_f2.grid(row=6, column=0, columnspan=1, padx=10, pady=40)

        self.quit_f2 = tk.Button(self.frame2,
                            text='Quit', 
                            command=self.quit,
                            bg="#9C9C9C",
                            padx=70,
                            pady=15,
                            font=("Gill Sans Ultra Bold", 15),
                            activebackground='#345',
                            activeforeground='white',
                            borderwidth=3,
                            relief='raised',
                            )
        self.quit_f2.grid(row=6, column=2, columnspan=1, padx=10, pady=40)

        self.leaderbord_f2 = tk.Button(self.frame2,
                            text='Leaderboard', 
                            command=self.change_to_leader_from_menu,
                            bg="#9C9C9C",
                            padx=40,
                            pady=15,
                            font=("Gill Sans Ultra Bold", 15),
                            activebackground='#345',
                            activeforeground='white',
                            borderwidth=3,
                            relief='raised',
                            )
        self.leaderbord_f2.grid(row=6, column=1, columnspan=1, padx=10, pady=40)

        self.frame2.pack(expand=True)

        # Creating the frame1 (game)
        self.frame1 = tk.Frame(self.root)
        self.frame1.config(bg="#CDAA7D")
          
        self.title_f1 = tk.Label(self.frame1, 
                            text="Type as fast as you can!", 
                            font=("Gill Sans Ultra Bold", 30),
                            bg="#CDAA7D",
                            fg="#8B1A1A")
        self.title_f1.grid(row=0, column=0, columnspan=2, padx=5, pady=30)

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

        self.input_f1 = tk.Entry(self.frame1, width=20, justify='center' ,font=("Gill Sans Ultra Bold", 20))
        self.input_f1.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        self.input_f1.bind("<KeyPress>", self.start)

        self.reset_f1 = tk.Button(self.frame1,
                            text='Reset', 
                            command=self.reset,
                            bg="#9C9C9C",
                            padx=70,
                            pady=15,
                            font=("Gill Sans Ultra Bold", 15),
                            activebackground='#345',
                            activeforeground='white',
                            borderwidth=3,
                            relief='raised',
                            )
        self.reset_f1.grid(row=4, column=0, columnspan=1, padx=5, pady=10)

        self.menu_f1 = tk.Button(self.frame1,
                            text='Menu', 
                            command=self.change_to_menu_from_game,
                            bg="#9C9C9C",
                            padx=70,
                            pady=15,
                            font=("Gill Sans Ultra Bold", 15),
                            activebackground='#345',
                            activeforeground='white',
                            borderwidth=3,
                            relief='raised',
                            )
        self.menu_f1.grid(row=4, column=1, columnspan=1, padx=5, pady=10)

        # Creating frame3 (leaderboard)
        self.frame3 = tk.Frame(self.root)
        self.frame3.config(bg="#CDAA7D")

        self.title_f3 = tk.Label(self.frame3, 
                            text="Leaderboard", 
                            font=("Gill Sans Ultra Bold", 30),
                            bg="#CDAA7D",
                            fg="#8B1A1A"
                            )
        self.title_f3.grid(row=0, column=1, columnspan=1, padx=5, pady=20)

        self.list_view_f3 = ttk.Treeview(self.frame3, 
                            column=('c1', 'c2', 'c3', 'c4'),
                            show='headings',
                            height=13,
                            selectmode='extended',
                            )
        self.style_f3 = ttk.Style()
        self.style_f3.theme_use('clam')
        self.style_f3.configure("Treeview.Heading",
                            font=("Gill Sans Ultra Bold", 15),
                            background="#CB7F19",
                            fieldbackground="#CB7F19",
                            )
        self.style_f3.configure("Treeview", 
                            background="#CBAD33",
                            fieldbackground="#CBAD33",
                            font=("Gill Sans Ultra Bold", 15),
                            rowheight=30
                            )
        self.list_view_f3.column("# 1", anchor=CENTER, stretch=False)
        self.list_view_f3.heading("# 1", text='Name')
        self.list_view_f3.column("# 2", anchor=CENTER, stretch=False)
        self.list_view_f3.heading("# 2", text='Mode')
        self.list_view_f3.column("# 3", anchor=CENTER, stretch=False)
        self.list_view_f3.heading("# 3", text='Accuracy')
        self.list_view_f3.column("# 4", anchor=CENTER, stretch=False)
        self.list_view_f3.heading("# 4", text='Time')
        for index, item in enumerate(Interface.list_leader):
            self.list_view_f3.insert('', 'end', text=str(index), values=item) 

        self.list_view_f3.grid(row=1, column=1, columnspan=1, padx=5, pady=20, sticky='nwes')

        self.menu_f3 = tk.Button(self.frame3,
                            text='Menu', 
                            command=self.change_to_menu_from_leader,
                            bg="#9C9C9C",
                            padx=70,
                            pady=15,
                            font=("Gill Sans Ultra Bold", 15),
                            activebackground='#345',
                            activeforeground='white',
                            borderwidth=3,
                            relief='raised',
                            )
        self.menu_f3.grid(row=2, column=1, columnspan=1, padx=5, pady=10)



        
        
        # Creating frame4 (final score)
        self.frame4 = tk.Frame(self.root)
        self.frame4.config(bg="#CDAA7D")

        self.title_f4 = tk.Label(self.frame4, 
                            text="This is your score!", 
                            font=("Gill Sans Ultra Bold", 30),
                            bg="#CDAA7D",
                            fg="#8B1A1A"
                            )
        self.title_f4.grid(row=0, column=0, columnspan=3, padx=5, pady=20)

        self.scores_label_f4 = tk.Label(self.frame4,
                            text=self.scores,
                            font=("Gill Sans Ultra Bold", 30),
                            bg="#CDAA7D"
                            )
        self.scores_label_f4.grid(row=1, column=0, columnspan=3, padx=5, pady=20)

        self.register_f4 = tk.Button(self.frame4,
                            text='Register score', 
                            command=self.insert_database,
                            bg="#9C9C9C",
                            padx=30,
                            pady=15,
                            font=("Gill Sans Ultra Bold", 15),
                            activebackground='#345',
                            activeforeground='white',
                            borderwidth=3,
                            relief='raised',
                            )
        self.register_f4.grid(row=4, column=0, columnspan=1, padx=10, pady=40)

        self.try_again_f4 = tk.Button(self.frame4,
                            text='Try again', 
                            command=self.change_to_game_from_score,
                            bg="#9C9C9C",
                            padx=50,
                            pady=15,
                            font=("Gill Sans Ultra Bold", 15),
                            activebackground='#345',
                            activeforeground='white',
                            borderwidth=3,
                            relief='raised',
                            )
        self.try_again_f4.grid(row=4, column=1, columnspan=1, padx=10, pady=40)

        self.menu_f4 = tk.Button(self.frame4,
                            text='Menu', 
                            command=self.change_to_menu_from_score,
                            bg="#9C9C9C",
                            padx=70,
                            pady=15,
                            font=("Gill Sans Ultra Bold", 15),
                            activebackground='#345',
                            activeforeground='white',
                            borderwidth=3,
                            relief='raised',
                            )
        self.menu_f4.grid(row=4, column=2, columnspan=1, padx=10, pady=40)
                
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
            self.root.after(1500, self.change_to_score_from_game)
            
    def time_thread(self):
        """This is a threading method that will run timer"""
        initial_time = time.time()
        while self.running:
            clock = time.time()
            self.time = clock - initial_time
            self.speed_f1.config(text=f'{self.time:.2f} seconds')

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

    def change_to_menu_from_game(self):
        """This method will change to menu screen from game screen"""
        self.frame2.pack(expand = True)
        self.frame1.forget()
        self.name_f2.focus_set()

    def change_to_score_from_game(self):
        """This method will change to final score screen from game screen"""
        self.frame4.pack(expand=True)
        self.frame1.forget()

    def change_to_game_from_score(self):
        """Thie method will change to game screen from final score screen"""
        self.frame1.pack(expand=True)
        self.frame4.forget()
        self.reset()
        self.input_f1.config(state='normal')
        self.input_f1.focus_get()

    def change_to_menu_from_score(self):
        """This method will change to menu screen from final score screen"""
        self.frame2.pack(expand=True)
        self.frame4.forget()
        self.name_f2.focus_set()

    def change_to_game_from_menu(self):
        """This method will change to game screen from menu screen"""
        if self.name_f2.get() != '' and self.difficulty_f2.get():
            self.frame1.pack(expand = True)
            self.frame2.forget()
            self.input_f1.focus_set()

    def change_to_leader_from_menu(self):
        """This method will change to leaderboard screen from menu screen"""
        self.frame3.pack(expand=True)
        self.frame2.forget()        

    def change_to_menu_from_leader(self):
        """This method will change to menu screen from leaderboard screen"""
        self.frame2.pack(expand=True)
        self.frame3.forget()

    def insert_database(self):
        """This method will insert a new or update a existent data in a MongoDB database"""
        client = MongoClient('localhost', 27017)
        database = client['speed-typing']
        records = database['records']
        data = {
            'name': self.name_f2.get(),
            'mode': '',
            'score_positive': self.scores[0], 
            'score_negative': self.scores[1],
            'accuracy': f'{(self.scores[0] / sum(self.scores))*100:.2f}%',
            'time': round(self.time, 2)
        }
        if records.find_one({'name': data.get('name')}):
            records.update_one({'name': self.name_f2.get()}, {
                '$set': {
                    'mode': '',
                    'score_positive': self.scores[0],
                    'score_negative': self.scores[1],
                    'accuracy': f'{(self.scores[0] / sum(self.scores))*100:.2f}%',
                    'time': round(self.time, 2)
                }
            })
        else:
            records.insert_one(data)


if __name__ == '__main__':
    Interface()