import tkinter as tk
from tkinter import ttk
from database import fetch_all_products, process_sale
from datetime import datetime
import sqlite3


# Function to open a new window for processing sales
def open_process_sale_window(app):
    sale_window = tk.Toplevel(app)  # Opens a new window
    sale_window.title("Process Sale")
    sale_window.geometry("700x800")  # Increased window size

    # Label for the title
    tk.Label(sale_window, text='Process Sale', font=('Arial', 16)).pack(pady=20)

    # Fetch products
    products = fetch_all_products()

    # Create a frame for the product search bar and list
    search_frame = tk.Frame(sale_window)
    search_frame.pack(pady=10, padx=10)

    # Search bar label and entry
    tk.Label(search_frame, text='Search Product:', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var, width=30)
    search_entry.grid(row=0, column=1, padx=10, pady=5)

    # Treeview for listing products with columns
    columns = ('Product ID', 'Product Name', 'Price', 'Stock')
    product_tree = ttk.Treeview(search_frame, columns=columns, show='headings', height=10)
    product_tree.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky='nsew')

    # Define column headings
    for col in columns:
        product_tree.heading(col, text=col)

    # Adjust column widths
    product_tree.column('Product ID', width=80)
    product_tree.column('Product Name', width=200)
    product_tree.column('Price', width=100)
    product_tree.column('Stock', width=100)

    # Function to filter products based on the search bar input
    def filter_products(event):
        search_term = search_var.get().lower()
        for row in product_tree.get_children():
            product_tree.delete(row)
        for product in products:
            if search_term in product[1].lower():
                product_tree.insert('', 'end', values=product)

    # Bind the search bar to update product list dynamically
    search_entry.bind('<KeyRelease>', filter_products)

    # Insert all products initially
    for product in products:
        product_tree.insert('', 'end', values=product)

    # Quantity label and entry
    tk.Label(sale_window, text='Quantity:', font=('Arial', 12)).pack(pady=5)
    quantity_entry = tk.Entry(sale_window)
    quantity_entry.pack(pady=5)

    # Process sale button
    def process_selected_product():
        try:
            selected_item = product_tree.selection()
            if not selected_item:
                raise ValueError('No product selected')
            product = product_tree.item(selected_item)['values']
            product_id = product[0]
            quantity = int(quantity_entry.get())
            if quantity <= 0:
                raise ValueError('Quantity must be greater than 0')

            process_sale(product_id, quantity)
            tk.messagebox.showinfo('Success', 'Sale processed successfully')
        except ValueError as ve:
            tk.messagebox.showerror('Error', str(ve))

    process_button = tk.Button(sale_window, text='Process Sale', command=process_selected_product)
    process_button.pack(pady=10)

    # Back button to return to the dashboard
    from views import show_dashboard
    back_button = tk.Button(sale_window, text="Back", command=lambda: show_dashboard(app))
    back_button.pack(pady=10)



# Function to retrieve sales for today, this month, and this year
def fetch_sales_for_period(period):
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()

    # Get today's date
    today = datetime.today()

    if period == 'today':
        cursor.execute("""
            SELECT sales.product_id, products.name, sales.quantity, sales.sale_price, sales.sale_date 
            FROM sales 
            JOIN products ON sales.product_id = products.id
            WHERE date(sale_date) = date(?)""", (today,))
    elif period == 'month':
        cursor.execute("""
            SELECT sales.product_id, products.name, sales.quantity, sales.sale_price, sales.sale_date 
            FROM sales 
            JOIN products ON sales.product_id = products.id
            WHERE strftime('%Y-%m', sale_date) = strftime('%Y-%m', ?)""", (today,))
    elif period == 'year':
        cursor.execute("""
            SELECT sales.product_id, products.name, sales.quantity, sales.sale_price, sales.sale_date 
            FROM sales 
            JOIN products ON sales.product_id = products.id
            WHERE strftime('%Y', sale_date) = strftime('%Y', ?)""", (today,))

    sales = cursor.fetchall()
    conn.close()

    return sales


## Function to view sales for today, this month, and this year
def view_sales_for_day(app):
    sales_window = tk.Toplevel(app)  # Create a new window for sales
    sales_window.title("Sales Data")
    sales_window.geometry("700x700")

    # Frame to hold the sales list
    sales_frame = tk.Frame(sales_window)
    sales_frame.pack(pady=20, fill="both", expand=True)

    # Function to display sales
    def display_sales(sales, period_label):
        for widget in sales_frame.winfo_children():
            widget.destroy()

        tk.Label(sales_frame, text=f"Sales for {period_label}", font=('Arial', 14)).pack(pady=10)

        if not sales:
            tk.Label(sales_frame, text="No sales data found.", font=('Arial', 12)).pack(pady=10)
        else:
             for sale in sales:
                 product_id, name, quantity, sale_price, sale_date = sale  # Unpack 5 values now
                 sale_info = (f"Product ID: {product_id}, Product Name: {name}, "
                         f"Quantity: {quantity}, Sale Price: ${sale_price:.2f}, Date: {sale_date}")
                 tk.Label(sales_frame, text=sale_info, font=('Arial', 12)).pack(pady=2)
            
            
            
    # Fetch product name based on product_id
    def fetch_product_name(product_id):
        conn = sqlite3.connect('pos.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM products WHERE id=?", (product_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 'Unknown'

    # Fetch sales data
    sales_data = {
        'today': fetch_sales_for_period('today'),
        'month': fetch_sales_for_period('month'),
        'year': fetch_sales_for_period('year')
    }

    # Display sales for today by default
    display_sales(sales_data['today'], 'today')

    # Buttons to switch between today's, this month's, and this year's sales
    tk.Button(sales_window, text="Today's Sales", command=lambda: display_sales(sales_data['today'], 'today')).pack(pady=5)
    tk.Button(sales_window, text="This Month's Sales", command=lambda: display_sales(sales_data['month'], 'this month')).pack(pady=5)
    tk.Button(sales_window, text="This Year's Sales", command=lambda: display_sales(sales_data['year'], 'this year')).pack(pady=5)
