from tkinter import ttk, messagebox

class AddItemForm(ttk.Frame):
    def __init__(self, parent, app, restaurant_id):
        super().__init__(parent)
        self.app = app
        self.db = app.db
        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self
        self.restaurant_id = restaurant_id
        self.create_widgets()
        
    def create_widgets(self):

        ttk.Label(self.main_frame, text="Add Menu Item", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        fields = [
            ("Item Name", "name"),
            ("Description", "description"),
            ("Price", "price"),
            ("Availability", "availability"),
        ]

        self.entries = {}
        for i, (label, field) in enumerate(fields, start=1):
            ttk.Label(self.main_frame, text=label + ":").grid(row=i, column=0, pady=10, sticky="e")
            if field == "availability":
                entry = ttk.Combobox(self.main_frame, values=["In Stock", "Out of Stock"])
            else:
                entry = ttk.Entry(self.main_frame)
            entry.grid(row=i, column=1, pady=10, sticky="w")
            self.entries[field] = entry

        ttk.Button(self.main_frame, text="Submit", command=self.add_item).grid(row=len(fields)+1, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back).grid(row=len(fields)+2, column=0, columnspan=2, pady=5)

    def add_item(self):
        from welcome.login.restaurant.manage_menu.manage_menu import ManageMenu
        data = {field: entry.get().strip() for field, entry in self.entries.items()}
        for field, value in data.items():
            if not value:
                messagebox.showerror("Error", f"{field.capitalize()} is required!")
                return

        try:
            insert_query = """
                INSERT INTO food_items (restaurant_id, name, description, price, availability)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.db.execute_query(insert_query, (
                self.restaurant_id,
                data["name"],
                data["description"],
                data["price"],
                data["availability"]
            ))
            messagebox.showinfo("Success", "Menu item added successfully!")
            self.app.show_frame(ManageMenu, restaurant_id=self.restaurant_id)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add menu item: {e}")

    def back(self):
        from welcome.login.restaurant.manage_menu.manage_menu import ManageMenu
        self.app.show_frame(ManageMenu, restaurant_id=self.restaurant_id)