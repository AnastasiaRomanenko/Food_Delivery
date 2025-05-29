from tkinter import ttk


class ShowCustomerOrder(ttk.Frame):
    def __init__(self, parent, app, user_id=14, restaurant_id=3, orders=[[14, 3, 2, 'Pizza "Chicago"', 40.0, 'mashrooms, salami, cheese'], [14, 3, 10, 'Cola', 5.0, '0.5l']]):
        super().__init__(parent)
        self.app = app
        self.user_id = user_id
        self.restaurant_id = restaurant_id
        self.orders = orders
        self.db = app.db 
        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self
        self.create_form()

    def create_form(self):

        self.tree = ttk.Treeview(self.main_frame, columns=("name", "food_item_name", "description", "total_amount"), show="headings")
        self.tree.heading("#1", text="Restaurant Name")
        self.tree.heading("#2", text="Food Item Name")
        self.tree.heading("#3", text="Description")
        self.tree.heading("#4", text="Amount")

        self.tree.column("name", width=100)
        self.tree.column("food_item_name", width=150)
        self.tree.column("description", width=200)
        self.tree.column("total_amount", width=100)

        self.tree.grid(row=0, column=0, columnspan=2, pady=10)
        self.load_orders()

        confirm_button = ttk.Button(self.main_frame, text="Confirm", command=self.confirm_order)
        confirm_button.grid(row=1, column=0, columnspan=2, pady=10)

        back_button = ttk.Button(self.main_frame, text="Back", command=self.back)
        back_button.grid(row=2, column=0, columnspan=2, pady=10)

    def load_orders(self):

        for i in range(len(self.orders)):
            food_item_id = self.orders[i][2]
            food_item_name = self.orders[i][3]
            total_amount = self.orders[i][4]
            food_item_description = self.orders[i][5]

            query_name = """
                SELECT name FROM restaurants WHERE id = %s
            """
            name = self.db.execute_query(query_name, (self.restaurant_id,))
            name = name[0][0]
            
            self.tree.insert("", "end", values=(name, food_item_name, food_item_description, total_amount))

    def confirm_order(self):
        from welcome.login.customer.choose_restaurant.show_menu.show_customer_order.confirm_order.confirm_order import ConfirmOrder
        self.app.show_frame(ConfirmOrder, self.user_id, self.restaurant_id, self.orders)
    
    def back(self):
        from welcome.login.customer.choose_restaurant.show_menu.show_menu import ShowMenu
        self.app.show_frame(ShowMenu, self.user_id, self.restaurant_id)

        
