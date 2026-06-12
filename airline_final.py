import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# 1. Connect to Database
mydb = sqlite3.connect("air_system.db")
mycursor = mydb.cursor()


# 2. Database Creation & Sample Setup
def setup_database():
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS passengers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, passport TEXT, destination TEXT)"
    )
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS tickets (class TEXT PRIMARY KEY, price INTEGER)"
    )
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS menu (item_id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT, price INTEGER)"
    )
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS food_bills (passenger_name TEXT, item_name TEXT, total_bill INTEGER)"
    )
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS luggage_bills (passenger_name TEXT, weight_kg REAL, total_bill INTEGER)"
    )

    mycursor.execute("SELECT COUNT(*) FROM tickets")
    if mycursor.fetchone()[0] == 0:
        mycursor.executemany(
            "INSERT INTO tickets VALUES (?, ?)",
            [("Economy", 5000), ("Business", 15000), ("First Class", 30000)],
        )
        mycursor.executemany(
            "INSERT INTO passengers (name, passport, destination) VALUES (?, ?, ?)",
            [
                ("Alice Smith", "A1234567", "London"),
                ("Bob Jones", "B9876543", "New York"),
            ],
        )
        mycursor.executemany(
            "INSERT INTO menu (item_name, price) VALUES (?, ?)",
            [("Veg Meal", 250), ("Chicken Sandwich", 180), ("Fruit Platter", 150)],
        )
        mycursor.executemany(
            "INSERT INTO food_bills VALUES (?, ?, ?)",
            [("Alice Smith", "Veg Meal", 250), ("Bob Jones", "Chicken Sandwich", 180)],
        )
        mycursor.executemany(
            "INSERT INTO luggage_bills VALUES (?, ?, ?)",
            [("Alice Smith", 23.5, 350), ("Bob Jones", 15.0, 0)],
        )
        mydb.commit()


setup_database()


# --- Premium Window Layout Helper ---
def apply_premium_window(win, title, width, height):
    win.title(title)
    win.geometry(f"{width}x{height}")
    win.configure(bg="#F8FAFC")


# --- Window Actions ---
def open_register_window():
    win = tk.Toplevel(root)
    apply_premium_window(win, "Passenger Registration", 420, 320)

    tk.Label(
        win,
        text="New Passenger Registration",
        font=("Segoe UI", 13, "bold"),
        bg="#F8FAFC",
        fg="#0F172A",
    ).pack(pady=15)

    frame = tk.Frame(win, bg="#F8FAFC")
    frame.pack(padx=20)

    lbl_style = {"font": ("Segoe UI", 10), "bg": "#F8FAFC", "fg": "#475569"}
    ent_style = {
        "font": ("Segoe UI", 10),
        "bd": 1,
        "relief": "solid",
        "bg": "#FFFFFF",
    }

    tk.Label(frame, text="Full Name:", **lbl_style).grid(
        row=0, column=0, sticky="w", pady=8, padx=5
    )
    ent_name = tk.Entry(frame, width=24, **ent_style)
    ent_name.grid(row=0, column=1, pady=8, ipady=2)

    tk.Label(frame, text="Passport No:", **lbl_style).grid(
        row=1, column=0, sticky="w", pady=8, padx=5
    )
    ent_pass = tk.Entry(frame, width=24, **ent_style)
    ent_pass.grid(row=1, column=1, pady=8, ipady=2)

    tk.Label(frame, text="Destination:", **lbl_style).grid(
        row=2, column=0, sticky="w", pady=8, padx=5
    )
    ent_dest = tk.Entry(frame, width=24, **ent_style)
    ent_dest.grid(row=2, column=1, pady=8, ipady=2)

    def save():
        n = ent_name.get().strip()
        p = ent_pass.get().strip()
        d = ent_dest.get().strip()
        if n and p and d:
            mycursor.execute(
                "INSERT INTO passengers (name, passport, destination) VALUES (?, ?, ?)",
                (n, p, d),
            )
            mydb.commit()
            messagebox.showinfo("Saved", f"Passenger {n} recorded successfully!")
            win.destroy()
        else:
            messagebox.showerror("Error", "All entry fields are required!")

    tk.Button(
        win,
        text="Register Passenger",
        command=save,
        font=("Segoe UI", 10, "bold"),
        bg="#0F172A",
        fg="white",
        activebackground="#1E293B",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        padx=15,
        pady=6,
    ).pack(pady=20)


def open_view_passengers():
    win = tk.Toplevel(root)
    apply_premium_window(win, "Passenger Roster", 600, 400)

    tk.Label(
        win,
        text="Active Flight Passengers",
        font=("Segoe UI", 13, "bold"),
        bg="#F8FAFC",
        fg="#0F172A",
    ).pack(pady=10)

    tree = ttk.Treeview(
        win, columns=("1", "2", "3", "4"), show="headings", style="Custom.Treeview"
    )
    tree.heading("1", text="ID")
    tree.heading("2", text="Passenger Name")
    tree.heading("3", text="Passport No:")
    tree.heading("4", text="Destination")

    tree.column("1", width=60, anchor="center")
    tree.column("2", width=180)
    tree.column("3", width=140, anchor="center")
    tree.column("4", width=160)

    mycursor.execute("SELECT * FROM passengers")
    for data_row in mycursor.fetchall():
        tree.insert("", "end", values=data_row)
    tree.pack(fill="both", expand=True, padx=20, pady=15)


def open_ticket_prices():
    win = tk.Toplevel(root)
    apply_premium_window(win, "Fare Sheets", 400, 300)

    tk.Label(
        win,
        text="Cabin Ticket Pricing",
        font=("Segoe UI", 13, "bold"),
        bg="#F8FAFC",
        fg="#0F172A",
    ).pack(pady=10)

    tree = ttk.Treeview(
        win, columns=("1", "2"), show="headings", style="Custom.Treeview"
    )
    tree.heading("1", text="Cabin Class")
    tree.heading("2", text="Price (INR)")

    tree.column("1", width=180, anchor="center")
    tree.column("2", width=160, anchor="center")

    mycursor.execute("SELECT * FROM tickets")
    for data_row in mycursor.fetchall():
        tree.insert("", "end", values=(data_row[0], f"₹ {data_row[1]:,}"))
    tree.pack(fill="both", expand=True, padx=20, pady=15)


def open_food_menu():
    win = tk.Toplevel(root)
    apply_premium_window(win, "Cuisine Options", 420, 320)

    tk.Label(
        win,
        text="In-Flight Dining Menu",
        font=("Segoe UI", 13, "bold"),
        bg="#F8FAFC",
        fg="#0F172A",
    ).pack(pady=10)

    tree = ttk.Treeview(
        win, columns=("1", "2", "3"), show="headings", style="Custom.Treeview"
    )
    tree.heading("1", text="Item ID")
    tree.heading("2", text="Dish Name")
    tree.heading("3", text="Price")

    tree.column("1", width=70, anchor="center")
    tree.column("2", width=200)
    tree.column("3", width=90, anchor="center")

    mycursor.execute("SELECT * FROM menu")
    for data_row in mycursor.fetchall():
        tree.insert("", "end", values=(data_row[0], data_row[1], f"₹ {data_row[2]:,}"))
    tree.pack(fill="both", expand=True, padx=20, pady=15)


def open_food_bills():
    win = tk.Toplevel(root)
    apply_premium_window(win, "Dining Ledger", 550, 450)

    tree = ttk.Treeview(
        win, columns=("1", "2", "3"), show="headings", style="Custom.Treeview"
    )
    tree.heading("1", text="Passenger Name")
    tree.heading("2", text="Cuisine Ordered")
    tree.heading("3", text="Total Bill")

    def load_food_data():
        for i in tree.get_children():
            tree.delete(i)
        mycursor.execute("SELECT * FROM food_bills")
        for data_row in mycursor.fetchall():
            tree.insert("", "end", values=(data_row[0], data_row[1], f"₹ {data_row[2]:,}"))

    load_food_data()
    tree.pack(fill="both", expand=True, padx=20, pady=10)

    add_f = tk.LabelFrame(
        win,
        text=" Log Food Order ",
        font=("Segoe UI", 9, "bold"),
        bg="#F8FAFC",
        fg="#334155",
    )
    add_f.pack(fill="x", padx=20, pady=15)

    lbl_s = {"bg": "#F8FAFC", "fg": "#475569", "font": ("Segoe UI", 9)}
    ent_s = {
        "font": ("Segoe UI", 9),
        "bd": 1,
        "relief": "solid",
        "bg": "#FFFFFF",
    }

    tk.Label(add_f, text="Name:", **lbl_s).grid(row=0, column=0, padx=4, pady=10)
    e_p = tk.Entry(add_f, width=13, **ent_s)
    e_p.grid(row=0, column=1, padx=4, ipady=2)

    tk.Label(add_f, text="Item:", **lbl_s).grid(row=0, column=2, padx=4, pady=10)
    e_i = tk.Entry(add_f, width=11, **ent_s)
    e_i.grid(row=0, column=3, padx=4, ipady=2)

    tk.Label(add_f, text="Cost:", **lbl_s).grid(row=0, column=4, padx=4, pady=10)
    e_c = tk.Entry(add_f, width=7, **ent_s)
    e_c.grid(row=0, column=5, padx=4, ipady=2)

    def add_food_entry():
        p, i, c = e_p.get().strip(), e_i.get().strip(), e_c.get().strip()
        if p and i and c:
            try:
                mycursor.execute(
                    "INSERT INTO food_bills VALUES (?, ?, ?)", (p, i, int(c))
                )
                mydb.commit()
                load_food_data()
                e_p.delete(0, tk.END)
                e_i.delete(0, tk.END)
                e_c.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Cost must be a clean number.")
        else:
            messagebox.showerror("Error", "Please fill all input fields.")

    tk.Button(
        add_f,
        text="Add",
        command=add_food_entry,
        bg="#0F172A",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        padx=10,
    ).grid(row=0, column=6, padx=6)


def open_luggage_bills():
    win = tk.Toplevel(root)
    apply_premium_window(win, "Cargo Manifest", 550, 450)

    tree = ttk.Treeview(
        win, columns=("1", "2", "3"), show="headings", style="Custom.Treeview"
    )
    tree.heading("1", text="Passenger")
    tree.heading("2", text="Baggage Weight")
    tree.heading("3", text="Excess Weight Fee")

    def load_luggage_data():
        for i in tree.get_children():
            tree.delete(i)
        mycursor.execute("SELECT * FROM luggage_bills")
        for data_row in mycursor.fetchall():
                        tree.insert("", "end", values=(data_row[0], f"{data_row[1]} kg", f"₹ {data_row[2]:,}"))

    load_luggage_data()
    tree.pack(fill="both", expand=True, padx=20, pady=10)

    add_f = tk.LabelFrame(
        win,
        text=" Log Cargo Load ",
        font=("Segoe UI", 9, "bold"),
        bg="#F8FAFC",
        fg="#334155"
    )
    add_f.pack(fill="x", padx=20, pady=15)

    lbl_s = {"bg": "#F8FAFC", "fg": "#475569", "font": ("Segoe UI", 9)}
    ent_s = {
        "font": ("Segoe UI", 9),
        "bd": 1,
        "relief": "solid",
        "bg": "#FFFFFF"
    }

    tk.Label(add_f, text="Passenger:", **lbl_s).grid(row=0, column=0, padx=4, pady=10)
    e_p = tk.Entry(add_f, width=15, **ent_s)
    e_p.grid(row=0, column=1, padx=4, ipady=2)

    tk.Label(add_f, text="Weight:", **lbl_s).grid(row=0, column=2, padx=4, pady=10)
    e_w = tk.Entry(add_f, width=10, **ent_s)
    e_w.grid(row=0, column=3, padx=4, ipady=2)

    def add_luggage_entry():
        p, w = e_p.get().strip(), e_w.get().strip()
        if p and w:
            try:
                weight = float(w)
                fee = int((weight - 15) * 100) if weight > 15 else 0
                mycursor.execute("INSERT INTO luggage_bills VALUES (?, ?, ?)", (p, weight, fee))
                mydb.commit()
                load_luggage_data()
                e_p.delete(0, tk.END)
                e_w.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Weight entries must be numeric.")
        else:
            messagebox.showerror("Error", "Please fill out passenger and cargo weight.")

    tk.Button(
        add_f,
        text="Calculate",
        command=add_luggage_entry,
        bg="#0F172A",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        padx=10
    ).grid(row=0, column=4, padx=10)


# --- Premium Application Dashboard Setup ---
root = tk.Tk()
root.title("Apex Flight Control Center")
root.geometry("440x540")
root.configure(bg="#FFFFFF")

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Custom.Treeview",
    background="#FFFFFF",
    foreground="#1E293B",
    rowheight=26,
    fieldbackground="#FFFFFF",
    font=("Segoe UI", 9)
)
style.configure(
    "Custom.Treeview.Heading",
    background="#F1F5F9",
    foreground="#0F172A",
    font=("Segoe UI", 9, "bold"),
    borderwidth=1
)

tk.Label(
    root,
    text="APEX AIRLINES SYSTEM",
    font=("Segoe UI", 14, "bold"),
    bg="#0F172A",
    fg="#FFFFFF",
    pady=16
).pack(fill="x")

opts = [
    ("Input Customer Data", open_register_window),
    ("Display List of Passengers", open_view_passengers),
    ("View Flight Ticket Prices", open_ticket_prices),
    ("Display Food Menu", open_food_menu),
    ("Display Passenger Food Bills", open_food_bills),
    ("Display Luggage Bills", open_luggage_bills)
]

for txt, cmd in opts:
    btn = tk.Button(
        root,
        text=txt,
        command=cmd,
        font=("Segoe UI", 9, "bold"),
        bg="#FFFFFF",
        fg="#1E293B",
        activebackground="#F1F5F9",
        activeforeground="#0F172A",
        bd=1,
        relief="solid",
        cursor="hand2",
        width=34,
        height=2
    )
    btn.pack(pady=6)

    def on_enter(e, b=btn):
        b.config(bg="#F1F5F9", fg="#0F172A")

    def on_leave(e, b=btn):
        b.config(bg="#FFFFFF", fg="#1E293B")

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

tk.Button(
    root,
    text="Exit Terminal System",
    command=root.quit,
    font=("Segoe UI", 9, "bold"),
    bg="#EF4444",
    fg="white",
    activebackground="#DC2626",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    width=34,
    height=2
).pack(pady=18)

root.mainloop()
mydb.close()

