from tkinter import ttk, messagebox

class ShowMenu(ttk.Frame):
    def __init__(self, parent, app, user_id, restaurant_id):
        super().__init__(parent)
        self.app = app
        self.user_id = user_id
        self.restaurant_id = restaurant_id
        self.db = app.db 
        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self
        self.orders = []
        self.create_form()
    
    def create_form(self):

        columns = ("name", "description", "price", "availability")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        
        self.tree.column("name", width=100)
        self.tree.column("description", width=100)
        self.tree.column("price", width=100)
        self.tree.column("availability", width=100)

        self.tree.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)
        self.load_menu_items()

        choose_item_button = ttk.Button(self.main_frame, text="Choose Item", command=self.choose_item)
        choose_item_button.grid(row=2, columnspan=2, column=0, pady=10)

        my_orders_button = ttk.Button(self.main_frame, text="My Order", command=self.show_customer_order)
        my_orders_button.grid(row=3, columnspan=2, pady=10)
        
        back_button = ttk.Button(self.main_frame, text="Back", command=self.back)
        back_button.grid(row=4, columnspan=2, column=0, pady=10)

    def load_menu_items(self):
        if not self.tree.winfo_exists():
            return
        
        self.tree.delete(*self.tree.get_children())
        
        query_food_items = """
            SELECT name, description, price, availability FROM food_items WHERE restaurant_id = %s
        """
        food_items = self.db.execute_query(query_food_items, (self.restaurant_id,))
        
        for item in food_items:
            self.tree.insert("", "end", values=item)

    def back(self):
        from welcome.login.customer.choose_restaurant.choose_restaurant import ChooseRestaurant
        self.app.show_frame(ChooseRestaurant, self.user_id)

    def get_selected_item(self):
        selected = self.tree.focus()
        if not selected:
            return None
        return self.tree.item(selected)["values"]
    
    def choose_item(self):
        selected_item = self.get_selected_item()
        if selected_item:
            if selected_item[3] == "In Stock":
                query_add_item = """
                    SELECT * FROM food_items WHERE restaurant_id = %s AND name = %s AND description = %s AND price = %s AND availability = %s
                """
                choose_item = self.db.execute_query(query_add_item, (self.restaurant_id, selected_item[0], selected_item[1], selected_item[2], selected_item[3]))
            
                if choose_item:
                    food_item_id = choose_item[0][0]
                    restaurant_id = choose_item[0][1]
                    food_item_name = choose_item[0][2]
                    total_amount = float(choose_item[0][3])
                    food_item_description = choose_item[0][5]
                    order = [self.user_id, restaurant_id, food_item_id, food_item_name, total_amount, food_item_description]
                    self.orders.append(order)
                else:
                    messagebox.showerror("Error", "No items found")
            else:
                messagebox.showerror("Error", "Item is not available")
        else:
            messagebox.showerror("Error", "No items found")

    def show_customer_order(self):
        from welcome.login.customer.choose_restaurant.show_menu.show_customer_order.show_customer_order import ShowCustomerOrder
        self.app.show_frame(ShowCustomerOrder, self.user_id, self.restaurant_id, self.orders)

