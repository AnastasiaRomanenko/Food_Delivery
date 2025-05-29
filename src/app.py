import tkinter as tk
from tkinter import ttk
from database.db_connection import DatabaseConnection

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GirlPower App")
        self.root.geometry("700x500")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.db = DatabaseConnection()
        self.clean_old_orders()
        self.current_frame = None

    def clean_old_orders(self):
        try:
            query = "DELETE FROM orders WHERE created_at < CURRENT_DATE"
            self.db.execute_query(query)
            print("Old orders deleted.")
        except Exception as e:
            pass
            

    def show_frame(self, frame_class, *args, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = frame_class(self.root, self, *args, **kwargs)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
    
    def get_centered_frame(self, top_margin=20):
        outer_frame = tk.Frame(self.root)
        outer_frame.grid(row=0, column=0, sticky="nsew")
        
        outer_frame.grid_rowconfigure(0, weight=0)
        outer_frame.grid_rowconfigure(1, weight=1)
        outer_frame.grid_columnconfigure(0, weight=1)
        tk.Frame(outer_frame, height=top_margin).grid(row=0, column=0)

        centered_frame = tk.Frame(outer_frame)
        centered_frame.grid(row=1, column=0, sticky="n")

        return centered_frame

    def run(self):
        self.root.mainloop()
        