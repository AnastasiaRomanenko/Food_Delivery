from tkinter import ttk

class CustomerActionForm(ttk.Frame):
    def __init__(self, parent, app, user_id):
        super().__init__(parent)
        self.app = app
        self.user_id = user_id
        self.db = app.db 
        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self
        self.create_form()
        
    def create_form(self):
        ttk.Label(self.main_frame, text="Customer", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(self.main_frame, text="Choose Restaurant", command=self.choose_restaurant).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="View Orders", command=self.view_orders).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back).grid(row=3, column=0, columnspan=2, pady=10)

    def choose_restaurant(self):
        from welcome.login.customer.choose_restaurant.choose_restaurant import ChooseRestaurant
        self.app.show_frame(ChooseRestaurant, self.user_id)

    def view_orders(self):
        from welcome.login.customer.view_orders.view_orders import ViewOrders
        self.app.show_frame(ViewOrders, self.user_id)

    def back(self):
        from welcome.login.login_form import LoginForm
        self.app.show_frame(LoginForm)