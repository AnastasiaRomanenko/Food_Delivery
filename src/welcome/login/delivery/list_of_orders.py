import tkinter as tk
from tkinter import ttk, messagebox
from database.db_connection import DatabaseConnection
import requests

mode_to_port = {
    "driving": 8091,
    "cycling": 8092,
    "foot": 8093
}

def get_coordinates(address):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': address, 'format': 'json', 'limit': 1}
    headers = {'User-Agent': 'YourAppNameHere'}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if not data:
        return None
    return float(data[0]['lon']), float(data[0]['lat'])

def get_local_osrm_route(origin, destination, profile):
    base_url = f"http://localhost:{mode_to_port[profile]}/route/v1/{profile}/"
    coordinates = f"{origin[0]},{origin[1]};{destination[0]},{destination[1]}"
    response = requests.get(base_url + coordinates, params={"overview": "false"})
    data = response.json()

    if response.status_code != 200 or data.get("code") != "Ok":
        raise Exception("Error fetching data from OSRM API")

    route = data["routes"][0]
    return {
        "distance_km": round(route["distance"] / 1000, 2),
        "duration_min": round(route["duration"] / 60, 1)
    }

class ListOfOrders(tk.Frame):
    def __init__(self, parent, app, delivery_personnel_id=15):
        super().__init__(parent)
        self.app = app
        self.db = app.db
        self.delivery_personnel_id = delivery_personnel_id
        self.main_frame = self.app.get_centered_frame()
        self.main_frame.master = self
        self.tree = None
        self.create_form()

    def create_form(self):

        self.tree = ttk.Treeview(self.main_frame, columns=("name", "restaurant_address", "customer_name", "customer_address", "total_amount", "payment_method"), show="headings")
        for idx, heading in enumerate(["Restaurant Name", "Restaurant Address", "Customer Name", "Customer Address", "Amount", "Payment Method"], start=1):
            self.tree.heading(f"#{idx}", text=heading)

        self.tree.column("#1", width=100)
        self.tree.column("#2", width=150)
        self.tree.column("#3", width=100)
        self.tree.column("#4", width=150)
        self.tree.column("#5", width=50)
        self.tree.column("#6", width=100)

        self.tree.grid(row=0, column=0, sticky="nsew", pady=10)

        ttk.Button(self.main_frame, text="Reload Orders", command=self.reload_orders).grid(row=1, column=0, pady=10)
        ttk.Button(self.main_frame, text="Choose Order", command=self.choose_order).grid(row=2, column=0, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back).grid(row=3, column=0, pady=10)

        self.load_orders()

    def reload_orders(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_form()
        self.load_orders()

    def load_orders(self):
        if not self.tree.winfo_exists():
            return

        self.tree.delete(*self.tree.get_children())

        query_vehicle = "SELECT vehicle_type FROM deliverypersonnel WHERE id = %s"
        vehicle_type = self.db.execute_query(query_vehicle, (self.delivery_personnel_id,))[0][0]

        query = """
            SELECT r.name, r.address, u.full_name, c.address, o.total_amount, o.payment_method
            FROM orders o
            JOIN restaurants r ON o.restaurant_id = r.id    
            JOIN customers c ON o.customer_id = c.id
            JOIN users u ON o.customer_id = u.id
            WHERE o.status = 'Accepted by Restaurant'
        """
        orders = self.db.execute_query(query)

        for order in orders:
            origin = get_coordinates(order[1])
            destination = get_coordinates(order[3])
            if not origin or not destination:
                continue

            durations = [get_local_osrm_route(origin, destination, m)["duration_min"] for m in ["driving", "cycling", "foot"]]

            for duration, mode in zip(durations, ["driving", "cycling", "foot"]):
                if duration > 10 and vehicle_type == "Car":
                    self.tree.insert("", "end", values=order)
                    break
                elif 10 < duration < 20 and vehicle_type == "Bike":
                    self.tree.insert("", "end", values=order)
                    break
                elif duration < 10 and vehicle_type == "By Foot":
                    self.tree.insert("", "end", values=order)
                    break

    def get_selected_order(self):
        selected = self.tree.focus()
        return self.tree.item(selected)["values"] if selected else None

    def choose_order(self):
        from welcome.login.delivery.accepted_order.accepted_order import AcceptedOrder

        selected_order = self.get_selected_order()
        if not selected_order:
            messagebox.showerror("Error", "Please select an order")
            return

        query_restaurant_id = "SELECT id FROM restaurants WHERE name = %s AND address = %s"
        restaurant_id = self.db.execute_query(query_restaurant_id, (selected_order[0], selected_order[1]))[0]

        query_customer_id = "SELECT id FROM users WHERE full_name = %s"
        customer_id = self.db.execute_query(query_customer_id, (selected_order[2],))[0][0]

        query_customer_address = "SELECT address FROM customers WHERE id = %s"
        customer_address = self.db.execute_query(query_customer_address, (customer_id,))[0][0]

        if customer_address != selected_order[3]:
            messagebox.showerror("Error", "Customer address does not match")
            return

        query_order_id = """
            SELECT id FROM orders WHERE restaurant_id = %s AND customer_id = %s AND total_amount = %s AND payment_method = %s
        """
        order_id = self.db.execute_query(query_order_id, (restaurant_id, customer_id, selected_order[4], selected_order[5]))[0][0]

        self.db.execute_query("UPDATE orders SET delivery_personnel_id = %s WHERE id = %s", (self.delivery_personnel_id, order_id))
        self.db.execute_query("UPDATE orders SET status = %s WHERE id = %s", ("Accepted by Delivery Person", order_id))

        messagebox.showinfo("Success", "Order accepted successfully")
        self.app.show_frame(AcceptedOrder, order_id)

    def back(self):
        from welcome.welcome_form import WelcomeForm
        self.app.show_frame(WelcomeForm)