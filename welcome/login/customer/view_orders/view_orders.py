from tkinter import ttk, messagebox

class ViewOrders(ttk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent)
        self.app = app
        self.user_id = user_id
        self.db = app.db 
        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self
        self.create_form()

        
    def create_form(self):
        ttk.Label(self.main_frame, text="Your current order").grid(row=0, column=0, sticky="nsew")

        self.tree = ttk.Treeview(self.main_frame, columns=("order_id", "name", "restaurant_address", "total_amount", "payment_method", "status"), show="headings")
        self.tree.heading("#1", text="Order ID")
        self.tree.heading("#2", text="Restaurant Name")
        self.tree.heading("#3", text="Restaurant Address")
        self.tree.heading("#4", text="Amount")
        self.tree.heading("#5", text="Payment Method")
        self.tree.heading("#6", text="Status")

        self.tree.column("#1", width=50)
        self.tree.column("#2", width=100)
        self.tree.column("#3", width=150)
        self.tree.column("#4", width=50)
        self.tree.column("#5", width=100)
        self.tree.column("#6", width=200)
        self.tree.grid(row=0, column=0, sticky="nsew", pady=10)

        ttk.Button(self.main_frame, text="Reload statuses", command=self.reload_status).grid(row=1, column=0, pady=10)
        ttk.Button(self.main_frame, text="Confirm accepting the order", command=self.accept_order).grid(row=2, column=0, pady=10)
        ttk.Button(self.main_frame, text="New order", command=self.new_order).grid(row=3, column=0, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back).grid(row=4, column=0, pady=10)

        self.load_order()

    def reload_status(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_form()

    def accept_order(self):
        selected_order = self.get_selected_order()
        if not selected_order:
            messagebox.showwarning("Warning", "Please select an order to accept.")
            return
        if selected_order[5] == 'Delivered':
            query = """
                UPDATE orders SET status = %s WHERE id = %s and status = 'Delivered'
            """
            self.db.execute_query(query, ("Accepted by Customer", selected_order[0],))
            messagebox.showinfo("Success", "Order accepted successfully.")
        else:
            messagebox.showwarning("Warning", "Order is not in a state that can be accepted.")
    
    def get_selected_order(self):
        selected = self.tree.focus()
        if not selected:
            return None
        return self.tree.item(selected)["values"]

    
    def load_order(self):
        if not self.tree.winfo_exists():
            return
        
        self.tree.delete(*self.tree.get_children())

        query_costomer_orders = """
            SELECT * FROM orders o WHERE o.customer_id = %s
        """
        orders = self.db.execute_query(query_costomer_orders, (self.user_id,))
        for order in orders:
            query_restaurant_name_and_address = """
                SELECT name, address from restaurants where id = %s 
            """
            restaurant_name_and_address = self.db.execute_query(query_restaurant_name_and_address, (order[2],))
            if order:
                self.tree.insert("", "end", values=(order[0], restaurant_name_and_address[0][0], restaurant_name_and_address[0][1], order[5], order[7], order[4]))
    
    def new_order(self):
        from welcome.login.customer.choose_restaurant.choose_restaurant import ChooseRestaurant
        self.app.show_frame(ChooseRestaurant, self.user_id)

    def back(self):
        from welcome.login.customer.customer_action_form import CustomerActionForm
        self.app.show_frame(CustomerActionForm, self.user_id)

    



        