import psycopg2
import tkinter as tk
from tkinter import messagebox, ttk

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="your_dbname",
            user="your_user",
            password="your_password",
            host="localhost",
            port="5432"
        )
        return conn
    except:
        messagebox.showerror("Connection Error", "Failed to connect to the database.")
        return None

def fetch_data():
    conn = connect_to_db()
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM your_table")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

    conn.close()

app = tk.Tk()
app.title("PostgreSQL Database GUI")

frame = ttk.Frame(app)
frame.pack(padx=10, pady=10)

tree = ttk.Treeview(frame, columns=("column1", "column2"), show="headings")
tree.heading("column1", text="Column 1")
tree.heading("column2", text="Column 2")
tree.pack()

fetch_button = tk.Button(app, text="Fetch Data", command=fetch_data)
fetch_button.pack(pady=20)

app.mainloop()
```