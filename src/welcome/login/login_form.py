from tkinter import ttk

class LoginForm(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.db = self.app.db 
        
        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self
        self.create_widgets()
        
    def create_widgets(self):
        ttk.Label(self.main_frame, text="Login Form", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        fields = [
            ("Username", "username"),
            ("Password", "password")
        ]
        
        self.entries = {}
        for i, (label, field) in enumerate(fields, start=0):
            ttk.Label(self.main_frame, text=label + ":").grid(row=2*i+1, column=0, pady=10)
            entry = ttk.Entry(self.main_frame)
            entry.grid(row=(i+1)*2, column=0, pady=10)
            self.entries[field] = entry
        
        self.entries["password"].config(show="*")

        ttk.Button(self.main_frame, text="Login", command=self.login).grid(row=len(fields)+3, column=0, columnspan=2, pady=10)
        back_button = ttk.Button(self.main_frame, text="Back", command=self.back)
        back_button.grid(row=len(fields)+4, column=0, columnspan=2, pady=10)
        
    def login(self):
        from tkinter import messagebox
        from welcome.login.customer.customer_action_form import CustomerActionForm
        from welcome.login.restaurant.restaurant_action_form import RestaurantActionForm
        from welcome.login.delivery.list_of_orders import ListOfOrders

        username = self.entries["username"].get()
        password = self.entries["password"].get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required!")
            return
        
        query_user = """
            SELECT * FROM users WHERE username = %s AND password = %s
        """
        user = self.db.execute_query(query_user, (username, password))

        query_restaurant = """
            SELECT * FROM restaurants WHERE username = %s AND password = %s
        """
        restaurant = self.db.execute_query(query_restaurant, (username, password))
        
        if user:
            messagebox.showinfo("Success", "Login successful!")
            query_user_id = """
                SELECT * FROM users WHERE username = %s AND password = %s
            """
            user = self.db.execute_query(query_user_id, (username, password))
            user_id = user[0][0]
            
            if user[0][6] == "Customer":
                self.app.show_frame(CustomerActionForm, user_id)
            elif user[0][6] == "Delivery":
                self.app.show_frame(ListOfOrders, user_id)
        elif restaurant:
            messagebox.showinfo("Success", "Login successful!")
            self.app.show_frame(RestaurantActionForm, restaurant[0][0])
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def back(self):
        from welcome.welcome_form import WelcomeForm
        self.app.show_frame(WelcomeForm)
