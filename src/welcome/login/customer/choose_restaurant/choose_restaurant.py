import tkinter as tk
from tkinter import ttk, messagebox
from database.db_connection import DatabaseConnection
from welcome.login.customer.choose_restaurant.show_menu.show_menu import ShowMenu

class ChooseRestaurant(ttk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent)
        self.app = app
        self.user_id = user_id
        self.db = app.db 
        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self
        
        self.create_form()

    def create_form(self):   
        ttk.Label(self.main_frame, text="Choose Restaurant", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        columns = ("name", "address", "phone", "email", "website")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        
        self.tree.column("name", width=50)
        self.tree.column("address", width=100)
        self.tree.column("phone", width=100)
        self.tree.column("email", width=100)
        self.tree.column("website", width=100)
        

        self.tree.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)
        self.load_restaurants()

        choose_restaurant_button = ttk.Button(self.main_frame, text="Choose Restaurant", command=self.choose_restaurant)
        choose_restaurant_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back).grid(row=3, column=0, columnspan=2, padx=10, pady=10)


    def load_restaurants(self):
        if not self.tree.winfo_exists():
            return
        
        self.tree.delete(*self.tree.get_children())
        
        query_restaurant = """
            SELECT name, address, phone, email, website FROM restaurants
        """
        restaurants = self.db.execute_query(query_restaurant)

        if not restaurants:
            return

        for restaurant in restaurants:
            self.tree.insert("", "end", values=restaurant)

    def get_selected_restaurant(self):
        selected = self.tree.focus()
        if not selected:
            return None
        return self.tree.item(selected)["values"]
    
    def back(self):
        from welcome.login.customer.customer_action_form import CustomerActionForm
        self.app.show_frame(CustomerActionForm, self.user_id)

    def choose_restaurant(self):

        selected_restaurant = self.get_selected_restaurant()

        if not selected_restaurant:
            messagebox.showerror("Error", "Please select a restaurant")
            return
                
        query_restaurant_id = """
            SELECT id FROM restaurants WHERE name = %s AND address = %s AND phone = %s AND email = %s AND website = %s
        """
        restaurant_id = self.db.execute_query(query_restaurant_id, (selected_restaurant[0], selected_restaurant[1], str(selected_restaurant[2]), selected_restaurant[3], selected_restaurant[4]))
        self.app.show_frame(ShowMenu, self.user_id, restaurant_id[0])
    

        