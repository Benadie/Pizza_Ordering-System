from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3

class PizzaRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.index_html().encode())
        elif self.path == '/menu':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            menu = self.get_menu()
            self.wfile.write(json.dumps(menu).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        if self.path == '/order':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            order = json.loads(post_data.decode())
            response = self.place_order(order)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/add_pizza':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_pizza = json.loads(post_data.decode())
            response = self.add_pizza(new_pizza)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/update_pizza':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            pizza_data = json.loads(post_data.decode())
            response = self.update_pizza(pizza_data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/delete_pizza':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            pizza_data = json.loads(post_data.decode())
            response = self.delete_pizza(pizza_data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')



    def get_menu(self):
        conn = sqlite3.connect('pizza.db')
        c = conn.cursor()
        c.execute('SELECT * FROM pizzas')
        menu = c.fetchall()
        conn.close()
        return {'menu': menu}

    def place_order(self, order):
        pizza_id = order.get('pizza_id')
        return {'message': f'Order for pizza with ID {pizza_id} received!'}

    def add_pizza(self, new_pizza):
        conn = sqlite3.connect('pizza.db')
        c = conn.cursor()
        c.execute('INSERT INTO pizzas (name, price, ingredients) VALUES (?, ?, ?)', 
                  (new_pizza['name'], new_pizza['price'], new_pizza['ingredients']))
        conn.commit()
        conn.close()
        return {'message': 'New pizza added successfully!'}

    def update_pizza(self, pizza_data):
        conn = sqlite3.connect('pizza.db')
        c = conn.cursor()
        c.execute('UPDATE pizzas SET name = ?, price = ?, ingredients = ? WHERE id = ?', 
                  (pizza_data['name'], pizza_data['price'], pizza_data['ingredients'], pizza_data['id']))
        conn.commit()
        conn.close()
        return {'message': 'Pizza updated successfully!'}

    def delete_pizza(self, pizza_data):
        conn = sqlite3.connect('pizza.db')
        c = conn.cursor()
        c.execute('DELETE FROM pizzas WHERE id = ?', (pizza_data['id'],))
        conn.commit()
        conn.close()
        return {'message': 'Pizza deleted successfully!'}

def create_database():
    conn = sqlite3.connect('pizza.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pizzas
                (id INTEGER PRIMARY KEY,
                 name TEXT,
                 price REAL,
                 ingredients TEXT)''')

    pizzas = [
        ('Margherita', 80.99, 'Tomato, Mozzarella, Basil'),
        ('Mexican', 100.99, 'Tomato, Mozzarella, Chilli'),
        ('Vegetarian', 90.99, 'Tomato, Mozzarella, Mushrooms, Peppers, Onions'),
        ('Hawaiian', 110.99, 'Tomato, Mozzarella, Ham, Pineapple')
    ]

    c.execute('SELECT * FROM pizzas')
    if not c.fetchall():
        c.executemany('INSERT INTO pizzas (name, price, ingredients) VALUES (?, ?, ?)', pizzas)

    conn.commit()
    conn.close()

def run():
    create_database()
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, PizzaRequestHandler)
    print('Starting server on port 8000...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()