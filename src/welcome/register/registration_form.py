from tkinter import ttk, messagebox
from database.db_connection import DatabaseConnection

class RegistrationForm(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        self.db = app.db  
        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self
        self.create_form()
    
        
    def create_form(self):
        ttk.Label(self.main_frame, text="Registration Form", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
           
        self.fields = [
            ("Username", "username"),
            ("Email", "email"),
            ("Password", "password"),
            ("Full Name", "full_name"),
            ("Phone", "phone"),
            ("Role", "role")
        ]
        
        self.entries = {}
        for i, (label, field) in enumerate(self.fields, start=1):
            ttk.Label(self.main_frame, text=label + ":").grid(row=i, column=0, pady=10, sticky="e")
            if field == "role":
                entry = ttk.Combobox(self.main_frame, values=["Customer", "Delivery"])
                entry.bind("<<ComboboxSelected>>", self.update_dynamic_fields)
            else:
                entry = ttk.Entry(self.main_frame)
            entry.grid(row=i, column=1, pady=10, sticky="w")
            self.entries[field] = entry
        
        self.entries["password"].config(show="*")
        
        self.dynamic_frame = ttk.Frame(self.main_frame)
        self.dynamic_frame.grid(row=len(self.fields) + 1, column=0, columnspan=2, pady=10)
        
        self.register_button = ttk.Button(self.main_frame, text="Register", command=self.register)
        self.register_button.grid(row=len(self.fields) + 2, column=0, columnspan=2, pady=10)

        self.back_button = ttk.Button(self.main_frame, text="Back", command=self.back)
        self.back_button.grid(row=len(self.fields) + 3, column=0, columnspan=2, pady=10)

        self.update_dynamic_fields()
    
    def update_dynamic_fields(self, event=None):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        self.entries.pop("vehicle", None)
        self.entries.pop("address", None)
        
        role = self.entries["role"].get()
        if role == "Delivery":
            
            ttk.Label(self.dynamic_frame, text="Vehicle:").grid(row=0, column=0, pady=10, sticky="e")
            self.entries["vehicle"] = ttk.Combobox(self.dynamic_frame, values=["Bike", "Car", "By Foot"])
            self.entries["vehicle"].grid(row=0, column=1, pady=10, sticky="w")

        elif role == "Customer":
            ttk.Label(self.dynamic_frame, text="Address:").grid(row=0, column=0, pady=10, sticky="e")
            self.entries["address"] = ttk.Entry(self.dynamic_frame)
            self.entries["address"].grid(row=0, column=1, pady=10, sticky="w")

    def register(self):
        from welcome.login.login_form import LoginForm

        try:
            data = {field: entry.get().strip() for field, entry in self.entries.items()}
            
            for field, value in data.items():
                if not value:
                    messagebox.showerror("Error", f"{field.capitalize()} is required!")
                    return
            
            query = """
                INSERT INTO users (username, email, password, full_name, phone, role)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """
            user_id = self.db.execute_query_returning_id(query, (
                data["username"],
                data["email"],
                data["password"],
                data["full_name"],
                data["phone"],
                data["role"]
            ))

            if self.entries["role"].get() == "Delivery":
                query = """
                    INSERT INTO deliverypersonnel (id, vehicle_type)
                    VALUES (%s, %s)
                """
                self.db.execute_query(query, (  
                    user_id,
                    data["vehicle"],
                ))
            elif self.entries["role"].get() == "Customer":
                query = """
                    INSERT INTO customers (id, address)
                    VALUES (%s, %s)
                """
                self.db.execute_query(query, (
                    user_id,
                    data["address"],
                ))
            
            messagebox.showinfo("Success", "Registration successful!")
            
            self.app.show_frame(LoginForm)
            
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
    
    def back(self):
        from welcome.welcome_form import WelcomeForm
        self.app.show_frame(WelcomeForm)