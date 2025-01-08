import tkinter as tk
from views import show_dashboard

# Initialize the main application window
app = tk.Tk()
app.title("POS System")
app.geometry("400x400")

# Start the dashboard
show_dashboard(app)

# Start the main event loop
app.mainloop()
