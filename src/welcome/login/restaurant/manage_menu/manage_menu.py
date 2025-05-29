from tkinter import ttk, messagebox

class ManageMenu(ttk.Frame):
    def __init__(self, parent, app, restaurant_id):
        super().__init__(parent)
        self.app = app
        self.db = app.db
        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self
        self.restaurant_id = restaurant_id
        self.create_form()

    def create_form(self):

        ttk.Label(self.main_frame, text="Manage Menu", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

        columns = ("id", "name", "description", "price", "availability")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        self.tree.column("id", width=30)
        self.tree.column("name", width=100)
        self.tree.column("description", width=200)
        self.tree.column("price", width=60)
        self.tree.column("availability", width=100)

        self.tree.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=10)

        ttk.Button(self.main_frame, text="Add Item", command=self.add_item).grid(row=2, column=0, padx=5, pady=10)
        ttk.Button(self.main_frame, text="Update Item", command=self.update_item).grid(row=2, column=1, padx=5, pady=10)
        ttk.Button(self.main_frame, text="Delete Item", command=self.delete_item).grid(row=2, column=2, padx=5, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back).grid(row=2, column=3, padx=5, pady=10)

        self.load_menu_items()

    def load_menu_items(self):
        if not self.tree.winfo_exists():
            return
        self.tree.delete(*self.tree.get_children())

        query = """
            SELECT id, name, description, price, availability
            FROM food_items
            WHERE restaurant_id = %s
        """
        items = self.db.execute_query(query, (self.restaurant_id,))
        if not items:
            return
        for item in items:
            self.tree.insert("", "end", values=item)

    def get_selected_item(self):
        selected = self.tree.focus()
        if not selected:
            return None
        return self.tree.item(selected)["values"]

    def add_item(self):
        from welcome.login.restaurant.manage_menu.add_item_form import AddItemForm
        self.app.show_frame(AddItemForm, restaurant_id=self.restaurant_id)

    def update_item(self):
        from welcome.login.restaurant.manage_menu.edit_item_form import EditItemForm
        selected_item = self.get_selected_item()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to update")
            return
        self.app.show_frame(EditItemForm, restaurant_id=self.restaurant_id, item_data=selected_item)

    def delete_item(self):
        selected_item = self.get_selected_item()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to delete")
            return
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this item?")
        if confirm:
            query = "DELETE FROM food_items WHERE id = %s"
            self.db.execute_query(query, (selected_item[0],))
            self.load_menu_items()

    def back(self):
        from welcome.login.restaurant.restaurant_action_form import RestaurantActionForm
        self.app.show_frame(RestaurantActionForm, restaurant_id=self.restaurant_id)