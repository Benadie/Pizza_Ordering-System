import requests
import json

def get_menu():
    url = 'http://localhost:8000/menu'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def place_order(pizza_id):
    url = 'http://localhost:8000/order'
    data = {'pizza_id': pizza_id}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def add_pizza(name, price, ingredients):
    url = 'http://localhost:8000/add_pizza'
    data = {'name': name, 'price': price, 'ingredients': ingredients}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def update_pizza(pizza_id, name, price, ingredients):
    url = 'http://localhost:8000/update_pizza'
    data = {'id': pizza_id, 'name': name, 'price': price, 'ingredients': ingredients}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def delete_pizza(pizza_id):
    url = 'http://localhost:8000/delete_pizza'
    data = {'id': pizza_id}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

if __name__ == '__main__':
    while True:
        print("\n1. View Menu\n2. Place Order\n3. Add Pizza\n4. Update Pizza\n5. Delete Pizza\n0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            menu = get_menu()
            if menu:
                print("Menu:")
                for pizza in menu['menu']:
                    print(f"{pizza[0]} - {pizza[1]} - R{pizza[2]} ({pizza[3]})")
            else:
                print("Failed to fetch menu from the server.")
        
        elif choice == '2':
            pizza_id = input("Enter the ID of the pizza you want to order: ")
            if not any(pizza[0] == int(pizza_id) for pizza in get_menu()['menu']):
                print("Invalid pizza ID. Please choose a valid ID from the menu.")
                continue
            order_response = place_order(pizza_id)
            if order_response:
                print(order_response['message'])
            else:
                print("Failed to place the order.")
        
        elif choice == '3':
            name = input("Enter the name of the new pizza: ")
            price = input("Enter the price of the new pizza: ")
            ingredients = input("Enter the ingredients of the new pizza: ")
            add_response = add_pizza(name, price, ingredients)
            if add_response:
                print(add_response['message'])
            else:
                print("Failed to add new pizza.")
        
        elif choice == '4':
            pizza_id = input("Enter the ID of the pizza you want to update: ")
            name = input("Enter the new name of the pizza: ")
            price = input("Enter the new price of the pizza: ")
            ingredients = input("Enter the new ingredients of the pizza: ")
            update_response = update_pizza(pizza_id, name, price, ingredients)
            if update_response:
                print(update_response['message'])
            else:
                print("Failed to update pizza.")
        
        elif choice == '5':
            pizza_id = input("Enter the ID of the pizza you want to delete: ")
            delete_response = delete_pizza(pizza_id)
            if delete_response:
                print(delete_response['message'])
            else:
                print("Failed to delete pizza.")
        
        elif choice == '0':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")