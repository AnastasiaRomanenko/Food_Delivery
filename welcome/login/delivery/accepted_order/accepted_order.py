import tkinter as tk
from tkinter import ttk, messagebox


class AcceptedOrder(tk.Frame):
    def __init__(self, parent, app, order_id=15):
        super().__init__(parent)
        self.app = app
        self.db = app.db
        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self
        self.order_id = order_id

        self.tree = None
        self.create_form()

    def create_form(self, delivery_stage=False):

        ttk.Label(self.main_frame, text="Your current order").grid(row=0, column=0, sticky="nsew")

        self.tree = ttk.Treeview(self.main_frame, columns=("name", "restaurant_address", "customer_name", "customer_address", "total_amount", "payment_method"), show="headings")
        self.tree.heading("#1", text="Restaurant Name")
        self.tree.heading("#2", text="Restaurant Address")
        self.tree.heading("#3", text="Customer Name")
        self.tree.heading("#4", text="Customer Address")
        self.tree.heading("#5", text="Amount")
        self.tree.heading("#6", text="Payment Method")

        self.tree.column("#1", width=100)
        self.tree.column("#2", width=150)
        self.tree.column("#3", width=100)
        self.tree.column("#4", width=150)
        self.tree.column("#5", width=50)
        self.tree.column("#6", width=100)
        self.tree.grid(row=1, column=0, sticky="nsew", pady=10)

        self.load_order()

        if delivery_stage:
            button = ttk.Button(self.main_frame, text="Verify delivery", command=self.verify_delivery)
        else:
            button = ttk.Button(self.main_frame, text="Verify pickup", command=self.verify_pickup)

        button.grid(row=2, column=0, pady=10)

        reload_button = ttk.Button(self.main_frame, text="Reload", command=self.reload_order)
        reload_button.grid(row=3, column=0, pady=10)

        
        back_button = ttk.Button(self.main_frame, text="Back", command=self.back)
        back_button.grid(row=4, column=0, pady=10)

    def reload_order(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_form()
        
    
    def load_order(self):
        if not self.tree.winfo_exists():
            return
        
        self.tree.delete(*self.tree.get_children())

        query_order = """
            SELECT * FROM orders o WHERE o.id = %s
        """
        order = self.db.execute_query(query_order, (self.order_id,))

        query_restaurant = """
            SELECT name, address FROM restaurants WHERE id = %s
        """
        restaurant = self.db.execute_query(query_restaurant, (order[0][2],))

        query_customer_name = """
            SELECT full_name FROM users WHERE id = %s
        """
        customer = self.db.execute_query(query_customer_name, (order[0][1],))
        query_customer_address = """
            SELECT address FROM customers WHERE id = %s
        """
        customer_address = self.db.execute_query(query_customer_address, (order[0][1],))
        if order:
            self.tree.insert("", "end", values=(restaurant[0][0], restaurant[0][1], customer[0][0], customer_address[0][0], order[0][5], order[0][7]))
    
    def get_selected_order(self):
        selected = self.tree.focus()
        if not selected:
            return None
        return self.tree.item(selected)["values"] 
      
    def verify_pickup(self):
        query_order = """
            SELECT status FROM orders o WHERE o.id = %s
        """
        order_status = self.db.execute_query(query_order, (self.order_id,))
        if order_status[0][0] == 'Given to Delivery Person':
            query_update_order = """
                UPDATE orders SET status = 'Picked by Delivery Person' WHERE id = %s
            """
            self.db.execute_query(query_update_order, (self.order_id,))
            messagebox.showinfo("Success", "Order pickup verified successfully.")
            self.create_delivery_button()
        else:
            messagebox.showwarning("Warning", "Order is not ready for pickup.")

    def verify_delivery(self):
        from welcome.login.delivery.list_of_orders import ListOfOrders
        
        query_order = """
            SELECT status FROM orders o WHERE o.id = %s
        """
        order_status = self.db.execute_query(query_order, (self.order_id,))
        if order_status[0][0] == 'Picked by Delivery Person':
            query_update_order = """
                UPDATE orders SET status = 'Delivered' WHERE id = %s and status = 'Picked by Delivery Person'
            """
            self.db.execute_query(query_update_order, (self.order_id,))
            messagebox.showinfo("Success", "Order delivery verified successfully.")
            self.app.show_frame(ListOfOrders)
        else:
            messagebox.showwarning("Warning", "Order is not ready for delivery.")
    
    def create_delivery_button(self):
        for widget in self.winfo_children():
            widget.destroy() 
        self.create_form(delivery_stage=True)


    def back(self):
        from welcome.login.delivery.list_of_orders import ListOfOrders
        self.app.show_frame(ListOfOrders)





