import tkinter as tk
from tkinter import ttk, messagebox
from database.db_connection import DatabaseConnection

class AddRestaurantForm(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.db = app.db
        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self
        self.create_form()

    def create_form(self):
        ttk.Label(self.main_frame, text="Add Restaurant", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2)

        fields = [
            ("Username", "username"),
            ("Restaurant Name", "name"),
            ("Address", "address"),
            ("Phone", "phone"),
            ("Password", "password"),
            ("Email", "email"),
            ("Website", "website"),
        ]

        self.entries = {}
        for i, (label, field) in enumerate(fields, start=1):
            ttk.Label(self.main_frame, text=label + ":").grid(row=i, column=0, pady=10, sticky="e")
            entry = ttk.Entry(self.main_frame)
            entry.grid(row=i, column=1, pady=10, sticky="w")
            self.entries[field] = entry

        self.entries["password"].config(show="*")

        submit_button = ttk.Button(self.main_frame, text="Submit", command=self.submit)
        submit_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)

        back_button = ttk.Button(self.main_frame, text="Back", command=self.back)
        back_button.grid(row=len(fields) + 2, column=0, columnspan=2, pady=10)

    def submit(self):
        data = {field: entry.get().strip() for field, entry in self.entries.items()}

        for field, value in data.items():
            if not value:
                messagebox.showerror("Error", f"{field.capitalize()} is required!")
                return

        query = """
            INSERT INTO restaurants (username, name, address, phone, password, email, website)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.db.execute_query(query, (
            data["username"],
            data["name"],
            data["address"],
            data["phone"],
            data["password"],
            data["email"],
            data["website"],
        ))

        messagebox.showinfo("Success", "Restaurant added successfully!")
        from welcome.login.login_form import LoginForm
        self.app.show_frame(LoginForm)

    def back(self):
        from welcome.welcome_form import WelcomeForm
        self.app.show_frame(WelcomeForm)