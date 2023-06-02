import pyodbc
from prettytable import PrettyTable
from tkinter import Tk, ttk
from ttkthemes import ThemedTk
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)
conn = pyodbc.connect(
    f'DRIVER={{SQL Server}};SERVER=MATEO\MSSQLSERVER01;DATABASE=FinalVeterinaria;UID=mateo_vet;PWD=Passw0rd')
cursor = conn.cursor()

query = "SELECT * FROM Mascotas"
cursor.execute(query)

# Fetch the column names
column_names = [column[0] for column in cursor.description]

# Create a PrettyTable object and set the column names
table = PrettyTable(column_names)

# Fetch the rows from the cursor and add them to the table
rows = cursor.fetchall()
for row in rows:
    table.add_row(row)

# Close the cursor and connection
cursor.close()
conn.close()

# Create a ThemedTk window from ttkthemes
window = ThemedTk(theme="equilux")  # Specify the theme name (e.g., "equilux")
window.configure(bg="#1e1e1e")  # Set background color

# Define custom styles for Treeview
style = ttk.Style()
style.theme_use("equilux")  # Use the "equilux" theme as a base

# Configure the heading style
style.configure("Custom.Treeview.Heading",
                background="#a2b1bd",  # Darker background color
                foreground="#d48a24",  # Brighter text color
                font=("Helvetica", 10))  # Custom font with increased brightness

# Apply the custom style to the Treeview widget
tree = ttk.Treeview(window, columns=column_names, show="headings", style="Custom.Treeview")
tree.pack(padx=10, pady=10, fill="both", expand=True)

# Configure column properties
column_padding = 5  # Adjust the padding between columns
column_width = 100  # Adjust the width of columns

# Add column headings to the Treeview
for col in column_names:
    tree.heading(col, text=col)

    # Configure column properties
    tree.column(col, width=column_width, anchor="center", minwidth=column_width, stretch=False)

# Add table rows to the Treeview
for row in table._rows:
    tree.insert("", "end", values=row)

# Start the Tkinter event loop
window.mainloop()
