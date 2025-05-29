from tkinter import ttk

class RestaurantActionForm(ttk.Frame):
    def __init__(self, parent, app, restaurant_id):
        super().__init__(parent)
        self.app = app
        self.restaurant_id = restaurant_id
        self.db = app.db 
        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self
        self.create_form()

    def create_form(self):

        ttk.Label(self.main_frame, text="Restaurant", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(self.main_frame, text="Manage Menu", command=self.manage_menu).grid(row=1, column=0, pady=10, padx=10)
        ttk.Button(self.main_frame, text="Manage Orders", command=self.manage_orders).grid(row=1, column=1, pady=10, padx=10)
        ttk.Button(self.main_frame, text="Back", command=self.back).grid(row=2, column=0, columnspan=2, pady=10, padx=10)

    def manage_menu(self):
        from welcome.login.restaurant.manage_menu.manage_menu import ManageMenu
        self.app.show_frame(ManageMenu, self.restaurant_id)

    def manage_orders(self):
        from welcome.login.restaurant.manage_orders.manage_orders import ManageOrdersForm
        self.app.show_frame(ManageOrdersForm, self.restaurant_id)

    def back(self):
        from welcome.login.login_form import LoginForm
        self.app.show_frame(LoginForm)