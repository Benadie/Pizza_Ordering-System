import tkinter as tk
from tkinter import messagebox
import requests
import json

class PizzaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pizza Ordering System")

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()

        menu_label = tk.Label(self.root, text="Pizza Ordering System", font=("Arial", 16))
        menu_label.pack(pady=10)

        view_menu_button = tk.Button(self.root, text="View Menu", command=self.view_menu)
        view_menu_button.pack(pady=5)

        place_order_button = tk.Button(self.root, text="Place Order", command=self.place_order)
        place_order_button.pack(pady=5)

        add_pizza_button = tk.Button(self.root, text="Add Pizza", command=self.add_pizza)
        add_pizza_button.pack(pady=5)

        update_pizza_button = tk.Button(self.root, text="Update Pizza", command=self.update_pizza)
        update_pizza_button.pack(pady=5)

        delete_pizza_button = tk.Button(self.root, text="Delete Pizza", command=self.delete_pizza)
        delete_pizza_button.pack(pady=5)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def view_menu(self):
        self.clear_frame()

        menu_label = tk.Label(self.root, text="Pizza Menu", font=("Arial", 16))
        menu_label.pack(pady=10)

        self.menu_listbox = tk.Listbox(self.root, width=50)
        self.menu_listbox.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=self.create_main_menu)
        back_button.pack(pady=5)

        self.load_menu()

    def load_menu(self):
        url = 'http://localhost:8000/menu'
        response = requests.get(url)
        if response.status_code == 200:
            menu = response.json()
            self.menu_listbox.delete(0, tk.END)
            for pizza in menu['menu']:
                self.menu_listbox.insert(tk.END, f"{pizza[0]} - {pizza[1]} - R{pizza[2]} ({pizza[3]})")
        else:
            messagebox.showerror("Error", "Failed to fetch menu from the server.")

    def place_order(self):
        self.clear_frame()

        order_label = tk.Label(self.root, text="Place an Order", font=("Arial", 16))
        order_label.pack(pady=10)

        pizza_id_label = tk.Label(self.root, text="Enter Pizza ID:")
        pizza_id_label.pack()

        self.pizza_id_entry = tk.Entry(self.root)
        self.pizza_id_entry.pack(pady=5)

        order_button = tk.Button(self.root, text="Order Pizza", command=self.submit_order)
        order_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=self.create_main_menu)
        back_button.pack(pady=5)

    def submit_order(self):
        pizza_id = self.pizza_id_entry.get()
        url = 'http://localhost:8000/order'
        data = {'pizza_id': pizza_id}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            order_response = response.json()
            messagebox.showinfo("Order Status", order_response['message'])
        else:
            messagebox.showerror("Error", "Failed to place the order.")

    def add_pizza(self):
        self.clear_frame()

        add_label = tk.Label(self.root, text="Add New Pizza", font=("Arial", 16))
        add_label.pack(pady=10)

        name_label = tk.Label(self.root, text="Pizza Name:")
        name_label.pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)

        price_label = tk.Label(self.root, text="Price:")
        price_label.pack()
        self.price_entry = tk.Entry(self.root)
        self.price_entry.pack(pady=5)

        ingredients_label = tk.Label(self.root, text="Ingredients (comma-separated):")
        ingredients_label.pack()
        self.ingredients_entry = tk.Entry(self.root)
        self.ingredients_entry.pack(pady=5)

        add_button = tk.Button(self.root, text="Add Pizza", command=self.submit_add_pizza)
        add_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=self.create_main_menu)
        back_button.pack(pady=5)

    def submit_add_pizza(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        ingredients = self.ingredients_entry.get()
        url = 'http://localhost:8000/add_pizza'  # Changed endpoint
        data = {'name': name, 'price': price, 'ingredients': ingredients}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            add_response = response.json()
            messagebox.showinfo("Add Status", add_response['message'])
        else:
            messagebox.showerror("Error", "Failed to add the pizza.")

    def update_pizza(self):
        self.clear_frame()

        update_label = tk.Label(self.root, text="Update Pizza", font=("Arial", 16))
        update_label.pack(pady=10)

        pizza_id_label = tk.Label(self.root, text="Pizza ID:")
        pizza_id_label.pack()
        self.update_pizza_id_entry = tk.Entry(self.root)
        self.update_pizza_id_entry.pack(pady=5)

        name_label = tk.Label(self.root, text="New Name:")
        name_label.pack()
        self.update_name_entry = tk.Entry(self.root)
        self.update_name_entry.pack(pady=5)

        price_label = tk.Label(self.root, text="New Price:")
        price_label.pack()
        self.update_price_entry = tk.Entry(self.root)
        self.update_price_entry.pack(pady=5)

        ingredients_label = tk.Label(self.root, text="New Ingredients (comma-separated):")
        ingredients_label.pack()
        self.update_ingredients_entry = tk.Entry(self.root)
        self.update_ingredients_entry.pack(pady=5)

        update_button = tk.Button(self.root, text="Update Pizza", command=self.submit_update_pizza)
        update_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=self.create_main_menu)
        back_button.pack(pady=5)

    def submit_update_pizza(self):
        pizza_id = self.update_pizza_id_entry.get()
        name = self.update_name_entry.get()
        price = self.update_price_entry.get()
        ingredients = self.update_ingredients_entry.get()
        url = 'http://localhost:8000/update_pizza'  # Changed endpoint
        data = {'id': pizza_id, 'name': name, 'price': price, 'ingredients': ingredients}
        headers = {'Content-Type': 'application/json'}
        response  = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            update_response = response.json()
            messagebox.showinfo("Update Status", update_response['message'])
        else:
            messagebox.showerror("Error", "Failed to update the pizza.")

    def delete_pizza(self):
        self.clear_frame()

        delete_label = tk.Label(self.root, text="Delete Pizza", font=("Arial", 16))
        delete_label.pack(pady=10)

        pizza_id_label = tk.Label(self.root, text="Pizza ID:")
        pizza_id_label.pack()
        self.delete_pizza_id_entry = tk.Entry(self.root)
        self.delete_pizza_id_entry.pack(pady=5)

        delete_button = tk.Button(self.root, text="Delete Pizza", command=self.submit_delete_pizza)
        delete_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=self.create_main_menu)
        back_button.pack(pady=5)

    def submit_delete_pizza(self):
        pizza_id = self.delete_pizza_id_entry.get()
        url = 'http://localhost:8000/delete_pizza'  # Changed endpoint
        data = {'id': pizza_id}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            delete_response = response.json()
            messagebox.showinfo("Delete Status", delete_response['message'])
        else:
            messagebox.showerror("Error", "Failed to delete the pizza.")

if __name__ == '__main__':
    root = tk.Tk()
    app = PizzaApp(root)
    root.mainloop()