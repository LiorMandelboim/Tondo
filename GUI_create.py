import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from main import Movie_Recommendation as MR

from PIL import Image, ImageTk
import requests
from bs4 import BeautifulSoup


class create_labeled_combobox(ttk.Frame):
    def __init__(self, parent, label_text, combobox_values, combobox_size=10):
        ttk.Frame.__init__(self , parent)
        self.label = ttk.Label(self, text=label_text)
        self.combobox = ttk.Combobox(self, values=combobox_values , width=combobox_size)
        self.label.pack(side="left" , padx=5)
        self.combobox.pack(side="right")

    def get_value(self):
        return self.combobox.get()

class create_labeled_entry(ttk.Frame):
        def __init__(self, parent, label_text, textbox_size=30):
            ttk.Frame.__init__(self , parent)
            self.label = ttk.Label(self, text=label_text)
            text = tk.StringVar()
            self.textbox = ttk.Entry(self, textvariable=text , width=textbox_size)
            self.label.pack(side="left" , padx=5)
            self.textbox.pack(side="right")
        
        def get_value(self):
             return self.textbox.get()
        


class Application:
    def __init__(self):
        self.root= tk.Tk()
        self.root.configure(background='Pink')
        self.root.title("Movie Recommendation Generator")
        self.MR = MR()
        self.create_widgets()
        self.root.mainloop()

    def execute(self):
        rating = self.rating.get_value() if self.rating.get_value() else None
        length = self.length.get_value() if self.length.get_value() else None
        director = self.director.get_value() if self.director.get_value() else None
        actor = self.actor.get_value() if self.actor.get_value() else None
        genre = self.genres.get_value() if self.genres.get_value() else None
        year = self.year.get_value() if self.year.get_value() else None
        pref = {'genres' : genre , 'director' : director , 'rating' : rating , 'year' : year ,
            'time' : length , 'actors' : actor}
        top_five_movies = self.MR.recommend(pref)
        self.winners_window(top_five_movies)

    def winners_window(self , top_five_movies):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Winners")
        self.new_window.configure(background='yellow')

                # Create headers for the table
        headers = ("Movie", "Match Score")

        style = ttk.Style()
        style.theme_use("clam")  # Use a built-in theme
        style.configure("Yellow.Treeview", background="yellow", foreground="black") 

        # Create Treeview widget for the table
        tree = ttk.Treeview(self.new_window, columns=headers, show="headings" , style="Yellow.Treeview")
        tree.pack()

        # Add headers to the table
        for header in headers:
            tree.heading(header, text=header)
        
        tree.column("Movie", width=250)


        for movie, rating in top_five_movies.items():
            tree.insert("", "end", values=(movie, rating))
    
    def create_widgets(self):
        self.top_label = tk.Label(self.root , text ="Movie Recommendation Generator" , font=("Arial Bold" , 30))
        self.top_label.pack(padx=20,pady=20)
        
        self.middle_frame = ttk.Frame(self.root)

        start_rate = 80  
        end_rate = 93    
        step_rate = 1    
        ratings= [x / 10 for x in range(start_rate, end_rate, step_rate)]
        self.rating = create_labeled_combobox(self.middle_frame, "Rating:", ratings)
        self.rating.pack(side="left" , pady=20)

        genres = self.MR.get_values('genres')
        self.genres = create_labeled_combobox(self.middle_frame, "Genre:", genres)
        self.genres.pack(side="left" , pady=20)
    
        length = ['60-90' , '90-120' , '120-150' , '150-180' , '180+']
        self.length = create_labeled_combobox(self.middle_frame , "Length(min):" , length)
        self.length.pack(side="left", pady=20)
        self.middle_frame.pack()

        self.year = create_labeled_entry(self.root ,"From Year:" )
        self.year.pack(pady=10)

        self.director = create_labeled_entry(self.root ,"Director:" )
        self.director.pack(pady=10)

        self.actor = create_labeled_entry(self.root ,"Actor:" )
        self.actor.pack(pady=10)

        self.button= ttk.Button(self.root, text = "Submit" , command=self.execute)
        self.button.pack(side="right" , pady=20)
    

Application()


