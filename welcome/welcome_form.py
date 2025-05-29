from tkinter import ttk

class WelcomeForm(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self

        self.create_widgets()
        
    def create_widgets(self):

        label = ttk.Label(self.main_frame, text="Welcome to the GirlPower application!", font=("Arial", 16, "bold"))
        label.grid(row=0, column=0, pady=20, sticky="nsew")

        login_button = ttk.Button(self.main_frame, text="Login", command=self.open_login)
        login_button.grid(row=1, column=0, pady=10)

        register_button = ttk.Button(self.main_frame, text="Register", command=self.open_registration)
        register_button.grid(row=2, column=0, pady=10)

        add_restaurant_button = ttk.Button(self.main_frame, text="Add Restaurant", command=self.open_add_restaurant)
        add_restaurant_button.grid(row=3, column=0, pady=10)

        exit_button = ttk.Button(self.main_frame, text="Exit", command=self.exit)
        exit_button.grid(row=4, column=0, pady=10)

    def exit(self):
        self.app.root.destroy()

    def open_login(self):
        from welcome.login.login_form import LoginForm
        self.app.show_frame(LoginForm)

    def open_registration(self):
        from welcome.register.registration_form import RegistrationForm
        self.app.show_frame(RegistrationForm)

    def open_add_restaurant(self):
        from welcome.add_restaurant.add_restaurant_form import AddRestaurantForm
        self.app.show_frame(AddRestaurantForm)