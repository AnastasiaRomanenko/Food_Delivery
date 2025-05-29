import tkinter as tk
from tkinter import ttk, messagebox
from welcome.login.restaurant.restaurant_action_form import RestaurantActionForm

class ManageOrdersForm(ttk.Frame):
    def __init__(self, parent, app, restaurant_id=3):
        super().__init__(parent)
        self.app = app
        self.restaurant_id = restaurant_id
        self.delivery_person_id = 0
        self.db = app.db
        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self

        self.selected_order_id = None
        self.details_frame = None

        self.create_form()

    def create_form(self):

        self.tree = ttk.Treeview(self.main_frame, columns=("order_id", "status"), show="headings")
        self.tree.heading("#1", text="Order ID")
        self.tree.heading("#2", text="Status")
        self.tree.column("#1", width=50)
        self.tree.column("#2", width=200)
        self.tree.grid(row=0, column=0, sticky="nsew", pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.show_order_details)

        self.load_orders()

        ttk.Button(self.main_frame, text="Reload Statuses", command=self.reload_status).grid(row=1, column=0, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back).grid(row=2, column=0, pady=10)

    def reload_status(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_form()

    def show_order_details(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        if self.details_frame:
            self.details_frame.destroy()

        order = self.tree.item(selected_item, "values")
        order_id, status = order[0], order[1]
        self.selected_order_id = order_id

        self.details_frame = ttk.LabelFrame(self.main_frame, text="Order Details", padding="10")
        self.details_frame.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        query = """
            SELECT o.delivery_personnel_id, f.id, f.name
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN food_items f ON oi.food_item_id = f.id
            WHERE o.id = %s
        """

        details = self.db.execute_query(query, (order_id,))
        if not details:
            ttk.Label(self.details_frame, text="No item details found").grid(row=0, column=0)
            return

        ttk.Label(self.details_frame, text=f"Order ID: {order_id}").grid(row=0, column=0, sticky="w")
        ttk.Label(self.details_frame, text=f"Current Status: {status}").grid(row=1, column=0, sticky="w")

        self.delivery_person_id = details[0][0]
        ttk.Label(self.details_frame, text=f"Delivery Person ID: {self.delivery_person_id}").grid(row=2, column=0, sticky="w")

        ttk.Label(self.details_frame, text="Items:").grid(row=3, column=0, sticky="w")
        for idx, detail in enumerate(details, start=4):
            item_id, item_name = detail[1], detail[2]
            ttk.Label(self.details_frame, text=f"  - {item_id}: {item_name}").grid(row=idx, column=0, sticky="w")

        ttk.Button(self.details_frame, text="Change Status", command=self.change_status).grid(row=idx + 1, column=0, pady=10)

    def change_status(self):
        if not self.selected_order_id:
            messagebox.showwarning("No selection", "Please select an order.")
            return

        query = "SELECT status FROM orders WHERE id = %s"
        status = self.db.execute_query(query, (self.selected_order_id,))
        status = status[0][0]

        if status == "Pending":
            new_status = "Accepted by Restaurant"
        elif status == "Accepted by Delivery Person":
            new_status = "Ready"
        elif status == "Ready":
            new_status = "Given to Delivery Person"
        else:
            new_status = ""
        
        if new_status:
            update_query = "UPDATE orders SET status = %s WHERE id = %s"
            self.db.execute_query(update_query, (new_status, self.selected_order_id))
            messagebox.showinfo("Status Updated", f"Status changed to: {new_status}")
            self.reload_status()

    def load_orders(self):
        if not self.tree.winfo_exists():
            return

        self.tree.delete(*self.tree.get_children())

        query = """
            SELECT id, status FROM orders
            WHERE restaurant_id = %s
        """
        orders = self.db.execute_query(query, (self.restaurant_id,))
        if orders:
            for order in orders:
                self.tree.insert("", "end", values=order)

    def back(self):
        self.app.show_frame(RestaurantActionForm, self.restaurant_id)