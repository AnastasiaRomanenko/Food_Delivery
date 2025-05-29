from tkinter import ttk, messagebox

class ConfirmOrder(ttk.Frame):
    def __init__(self, parent, app, user_id, restaurant_id, orders):
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
        
        confirmation_label = ttk.Label(self.main_frame, text="Please choose payment method below:", font=("Arial", 16))
        confirmation_label.grid(row=0, column=0, pady=10, columnspan=3)

        sum = 0

        for i in range(len(self.orders)):
            sum += self.orders[i][4]
        
        sum_to_pay_label = ttk.Label(self.main_frame, text="Sum to pay: " + str(sum))
        sum_to_pay_label.grid(row=1, column=0, pady=10, columnspan=3)

        payment_method_label = ttk.Label(self.main_frame, text="Payment method:")
        payment_method_label.grid(row=2, column=0, pady=10)

        self.payment_method_combobox = ttk.Combobox(self.main_frame, values=["Cash", "Card"])
        self.payment_method_combobox.grid(row=2, column=1, pady=10, columnspan=2)

        confirm_order_button = ttk.Button(self.main_frame, text="Confirm order", command=self.confirm_order)
        confirm_order_button.grid(row=3, column=0, pady=10, padx=10, columnspan=3)

        view_order_button = ttk.Button(self.main_frame, text="View Order", command=self.view_order)
        view_order_button.grid(row=4, column=0, pady=10, padx=10, columnspan=3)

        back_button = ttk.Button(self.main_frame, text="Back", command=self.back)
        back_button.grid(row=5, column=0, pady=10, columnspan=3)

    def confirm_order(self):
        payment_method = self.payment_method_combobox.get()
        total_amount = 0
        for i in range(len(self.orders)):
            total_amount += self.orders[i][4]

        query_insert_order = """
            INSERT INTO orders (customer_id, restaurant_id, status, total_amount, payment_method) VALUES (%s, %s, %s, %s, %s)
        """
        status = "Pending"
        self.db.execute_query(query_insert_order, (self.user_id, self.restaurant_id, status, total_amount, payment_method))
        
        query_insert_order_item = """
            INSERT INTO order_items (order_id, food_item_id) VALUES (%s, %s)
        """

        order_id = self.db.execute_query("SELECT id FROM orders WHERE customer_id = %s AND restaurant_id = %s AND status = %s AND total_amount = %s AND payment_method = %s", (self.user_id, self.restaurant_id, status, total_amount, payment_method))
        order_id = order_id[0][0]
        for i in range(len(self.orders)):
            self.db.execute_query(query_insert_order_item, (order_id, self.orders[i][2]))
        
        messagebox.showinfo("Success", "Order placed successfully")

    def view_order(self):
        from welcome.login.customer.view_orders.view_orders import ViewOrders
        self.app.show_frame(ViewOrders, self.user_id)

    def back(self):
        from welcome.login.customer.choose_restaurant.show_menu.show_customer_order.show_customer_order import ShowCustomerOrder
        self.app.show_frame(ShowCustomerOrder, self.user_id, self.restaurant_id, self.orders)
