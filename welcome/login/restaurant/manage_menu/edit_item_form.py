from tkinter import ttk, messagebox

class EditItemForm(ttk.Frame):
    def __init__(self, parent, app, restaurant_id, item_data):
        super().__init__(parent)
        self.app = app
        self.db = app.db
        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self
        self.restaurant_id = restaurant_id
        self.item_data = item_data

        self.create_widgets()

    def create_widgets(self):

        ttk.Label(self.main_frame, text="Edit Menu Item", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.main_frame, text="Name:").grid(row=1, column=0, pady=10, sticky="e")
        self.name_entry = ttk.Entry(self.main_frame)
        self.name_entry.grid(row=1, column=1, pady=10, sticky="w")
        self.name_entry.insert(0, self.item_data[1])

        ttk.Label(self.main_frame, text="Description:").grid(row=2, column=0, pady=10, sticky="e") 
        self.desc_entry = ttk.Entry(self.main_frame)
        self.desc_entry.grid(row=2, column=1, pady=10, sticky="w")
        self.desc_entry.insert(0, self.item_data[2])

        ttk.Label(self.main_frame, text="Price:").grid(row=3, column=0, pady=10, sticky="e")
        self.price_entry = ttk.Entry(self.main_frame)
        self.price_entry.grid(row=3, column=1, pady=10, sticky="w")
        self.price_entry.insert(0, self.item_data[3])

        ttk.Label(self.main_frame, text="Availability:").grid(row=4, column=0, pady=10, sticky="e")
        self.availability_entry = ttk.Entry(self.main_frame)
        self.availability_entry.grid(row=4, column=1, pady=10, sticky="w")
        self.availability_entry.insert(0, self.item_data[4])

        ttk.Button(self.main_frame, text="Save", command=self.save_item).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back).grid(row=6, column=0, columnspan=2, pady=5)    

    def save_item(self):
        from welcome.login.restaurant.manage_menu.manage_menu import ManageMenu
        name = self.name_entry.get()
        description = self.desc_entry.get()
        price = self.price_entry.get()
        availability = self.availability_entry.get()

        if not all([name, description, price, availability]):
            messagebox.showerror("Error", "All fields must be filled!")
            return

        query = """
            UPDATE food_items
            SET name = %s, description = %s, price = %s, availability = %s
            WHERE id = %s
        """
        self.db.execute_query(query, (name, description, price, availability, self.item_data[0]))
        messagebox.showinfo("Success", "Item updated successfully!")
        self.app.show_frame(ManageMenu, restaurant_id=self.restaurant_id)

    def back(self):
        from welcome.login.restaurant.manage_menu.manage_menu import ManageMenu
        self.app.show_frame(ManageMenu, restaurant_id=self.restaurant_id)