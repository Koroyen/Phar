import tkinter as tk
from tkinter import messagebox
from database import add_product, show_products, update_stock, generate_report

def add_product_ui(name_entry, price_entry, stock_entry):
    name = name_entry.get()
    try:
        price = float(price_entry.get())
        stock = int(stock_entry.get())
        add_product(name, price, stock)
        messagebox.showinfo('Success', 'Product added successfully')
    except ValueError:
        messagebox.showerror("Error", "Please enter valid price and stock.")

def view_products_ui(app):
    products = show_products()
    view_window = tk.Toplevel(app)
    view_window.title('Inventory')

    tk.Label(view_window, text='ID').grid(row=0, column=0)
    tk.Label(view_window, text='Name').grid(row=0, column=1)
    tk.Label(view_window, text='Price').grid(row=0, column=2)
    tk.Label(view_window, text='Stock').grid(row=0, column=3)

    for i, product in enumerate(products):
        tk.Label(view_window, text=product[0]).grid(row=i+1, column=0)
        tk.Label(view_window, text=product[1]).grid(row=i+1, column=1)
        tk.Label(view_window, text=product[2]).grid(row=i+1, column=2)
        tk.Label(view_window, text=product[3]).grid(row=i+1, column=3)

def process_sale_ui(product_id_entry, quantity_entry):
    try:
        product_id = int(product_id_entry.get())
        quantity = int(quantity_entry.get())
        if update_stock(product_id, quantity):
            messagebox.showinfo('Success', 'Sale processed successfully')
        else:
            messagebox.showerror('Error', 'Insufficient stock')
    except ValueError:
        messagebox.showerror("Error", "Please enter valid product ID and quantity.")

def view_report_ui(app):
    report = generate_report()
    report_window = tk.Toplevel(app)
    report_window.title('Report')

    report_text = tk.Text(report_window)
    report_text.insert(tk.END, report)
    report_text.pack()
