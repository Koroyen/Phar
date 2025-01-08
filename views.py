import tkinter as tk
from tkinter import messagebox
from database import add_product, show_products, generate_report
from sales import open_process_sale_window, view_sales_for_day  # Import both functions from sales.py

# Function to add a new product
def add_product_ui(app):
    clear_window(app)

    tk.Label(app, text='Add Product', font=('Arial', 16)).pack(pady=20)

    name_label = tk.Label(app, text='Product Name:', font=('Arial', 12))
    name_label.pack(pady=5)
    name_entry = tk.Entry(app)
    name_entry.pack(pady=5)

    price_label = tk.Label(app, text='Product Price:', font=('Arial', 12))
    price_label.pack(pady=5)
    price_entry = tk.Entry(app)
    price_entry.pack(pady=5)

    stock_label = tk.Label(app, text='Product Stock:', font=('Arial', 12))
    stock_label.pack(pady=5)
    stock_entry = tk.Entry(app)
    stock_entry.pack(pady=5)

    def submit_product():
        try:
            name = name_entry.get()
            price = float(price_entry.get())
            stock = int(stock_entry.get())

            if not name or price <= 0 or stock <= 0:
                raise ValueError

            add_product(name, price, stock)
            messagebox.showinfo('Success', 'Product added successfully')
            show_dashboard(app)  # Return to the dashboard
        except ValueError:
            messagebox.showerror('Error', 'Invalid input. Please fill all fields correctly.')

    submit_button = tk.Button(app, text='Add Product', command=submit_product)
    submit_button.pack(pady=10)

    back_button = tk.Button(app, text="Back", command=lambda: show_dashboard(app))
    back_button.pack(pady=10)

# Function to view all products in inventory
def view_products_ui(app):
    clear_window(app)

    # Fixing the typo: Corrected the closing parenthesis for the font tuple.
    tk.Label(app, text='Product Inventory', font=('Arial', 16)).pack(pady=20)

    products = show_products()
    if not products:
        tk.Label(app, text='No products found.').pack(pady=10)
    else:
        for product in products:
            tk.Label(app, text=f'ID: {product[0]}, Name: {product[1]}, Price: ${product[2]:.2f}, Stock: {product[3]}').pack()

    back_button = tk.Button(app, text="Back", command=lambda: show_dashboard(app))
    back_button.pack(pady=10)

# Function to view report of all products
def view_report_ui(app):
    clear_window(app)

    tk.Label(app, text='Inventory Report', font=('Arial', 16)).pack(pady=20)

    report = generate_report()
    report_label = tk.Label(app, text=report, justify=tk.LEFT)
    report_label.pack(pady=10)

    back_button = tk.Button(app, text="Back", command=lambda: show_dashboard(app))
    back_button.pack(pady=10)

# Function to clear the window
def clear_window(app):
    for widget in app.winfo_children():
        widget.destroy()

# Dashboard UI
def show_dashboard(app):
    clear_window(app)

    tk.Label(app, text='Welcome to POS Dashboard', font=('Arial', 16)).pack(pady=20)
    tk.Button(app, text='Add Product', width=20, command=lambda: add_product_ui(app)).pack(pady=10)
    tk.Button(app, text='View Inventory', width=20, command=lambda: view_products_ui(app)).pack(pady=10)

    # Pass show_dashboard as an argument when calling open_process_sale_window
    tk.Button(app, text='Process Sale', width=20, command=lambda: open_process_sale_window(app)).pack(pady=10)



    tk.Button(app, text='View Sales for Today', font=("Arial", 14), command=lambda: view_sales_for_day(app)).pack(pady=10)
    tk.Button(app, text='Generate Report', width=20, command=lambda: view_report_ui(app)).pack(pady=10)
