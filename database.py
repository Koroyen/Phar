
from tkinter import messagebox  # Make sure to import messagebox from tkinter
from datetime import datetime
import sqlite3



# # Path to your SQLite database file
# DATABASE_PATH = 'pos.db'

# def alter_sales_table():
#     conn = sqlite3.connect(DATABASE_PATH)
#     cursor = conn.cursor()

#     # Add the sale_price column to the sales table
#     try:
#         cursor.execute('ALTER TABLE products ADD COLUMN product_name TEXT')
#         conn.commit()
#         print("sale_price column added successfully!")
#     except sqlite3.OperationalError as e:
#         print(f"Error: {e}. The column might already exist.")

#     conn.close()
    
    
# # Call the function to alter the table
# alter_sales_table()


def create_connection():
    conn = sqlite3.connect('pos.db')
    return conn

# Fetch all products from the database
def fetch_all_products():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, price, stock FROM products')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Fetch and display all products
def show_products():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Generate report of all products
def generate_report():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    report = 'ID\tName\tPrice\tStock\n'
    for product in products:
        report += f'{product[0]}\t{product[1]}\t{product[2]}\t{product[3]}\n'
    return report

# Other functions like process_sale, create_table, etc.

# For example, add these functions if they are missing
def add_product(name, price, stock):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, price, stock) VALUES (?, ?, ?)', (name, price, stock))
    conn.commit()
    conn.close()

def process_sale(product_id, quantity):
    conn = create_connection()
    cursor = conn.cursor()

    # Fetch product details
    cursor.execute('SELECT price, stock FROM products WHERE id=?', (product_id,))
    product = cursor.fetchone()

    if product:
        price, stock = product
        if stock >= quantity:
            # Update stock
            cursor.execute('UPDATE products SET stock = stock - ? WHERE id = ?', (quantity, product_id))
            
            # Insert sale into sales table
            sale_price = price * quantity
            sale_date = datetime.now()  # Get the current date and time
            
            cursor.execute('INSERT INTO sales (product_id, quantity, sale_price, sale_date) VALUES (?, ?, ?, ?)',
               (product_id, quantity, sale_price, sale_date))
            
            conn.commit()
            messagebox.showinfo('Success', 'Sale processed successfully')
        else:
            messagebox.showerror('Error', 'Insufficient stock')
    else:
        messagebox.showerror('Error', 'Product not found')

    conn.close()

# Create the products table if it doesn't exist
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        price REAL NOT NULL,
                        stock INTEGER NOT NULL)''')
    conn.commit()
    conn.close()


# Initialize the tables
create_table()
