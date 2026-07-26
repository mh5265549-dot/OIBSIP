import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt

# Database setup
DB_NAME = "bmi_records.db"

def init_db():
    """Initializes the SQLite database and creates the records table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bmi_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to initialize database: {e}")
    finally:
        conn.close()

class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator & Tracker - Oasis Infobyte")
        self.root.geometry("450x580")
        self.root.resizable(False, False)
        
        # Initialize Database
        init_db()

        # --- UI STYLES & WIDGETS ---
        style = ttk.Style()
        style.theme_use('clam')

        # --- TITLE BANNER (Oasis Infobyte Internship Info) ---
        banner_frame = tk.Frame(root, bg="#2c3e50", pady=8)
        banner_frame.pack(fill="x")
        
        banner_name = tk.Label(banner_frame, text="Hashir Shoaib", font=("Arial", 11, "bold"), fg="white", bg="#2c3e50")
        banner_name.pack()
        
        banner_details = tk.Label(banner_frame, text="Track: Python Programming | Task 2: Advanced BMI Calculator", font=("Arial", 9), fg="#bdc3c7", bg="#2c3e50")
        banner_details.pack()

        # Main Header
        title_label = tk.Label(root, text="BMI Tracker & Analyzer", font=("Arial", 14, "bold"), fg="#2c3e50")
        title_label.pack(pady=10)

        # Input Frame
        input_frame = tk.LabelFrame(root, text=" User & Measurements ", font=("Arial", 10, "bold"), padx=15, pady=10)
        input_frame.pack(fill="x", padx=20, pady=5)

        # Username
        tk.Label(input_frame, text="Username:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(input_frame, font=("Arial", 10), width=20)
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)

        # Weight
        tk.Label(input_frame, text="Weight (kg):", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.weight_entry = tk.Entry(input_frame, font=("Arial", 10), width=20)
        self.weight_entry.grid(row=1, column=1, pady=5, padx=5)

        # Height
        tk.Label(input_frame, text="Height (m):", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.height_entry = tk.Entry(input_frame, font=("Arial", 10), width=20)
        self.height_entry.grid(row=2, column=1, pady=5, padx=5)

        # Action Buttons Frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=12)

        calc_btn = tk.Button(btn_frame, text="Calculate & Save", font=("Arial", 10, "bold"), bg="#27ae60", fg="white", padx=10, pady=5, command=self.calculate_and_save)
        calc_btn.grid(row=0, column=0, padx=10)

        chart_btn = tk.Button(btn_frame, text="View Trend Chart", font=("Arial", 10, "bold"), bg="#2980b9", fg="white", padx=10, pady=5, command=self.show_trend_chart)
        chart_btn.grid(row=0, column=1, padx=10)

        # Result Display Area
        result_frame = tk.LabelFrame(root, text=" Results ", font=("Arial", 10, "bold"), padx=15, pady=10)
        result_frame.pack(fill="x", padx=20, pady=5)

        self.bmi_label = tk.Label(result_frame, text="BMI: --", font=("Arial", 12))
        self.bmi_label.pack(anchor="w", pady=2)

        self.category_label = tk.Label(result_frame, text="Category: --", font=("Arial", 12, "bold"))
        self.category_label.pack(anchor="w", pady=2)

    def calculate_bmi(self, weight, height):
        """Calculates BMI value rounded to 2 decimal places."""
        return round(weight / (height ** 2), 2)

    def get_category(self, bmi):
        """Classifies BMI value into standard health categories."""
        if bmi < 18.5:
            return "Underweight", "#f39c12"  # Orange-Yellow
        elif 18.5 <= bmi <= 24.9:
            return "Normal", "#27ae60"     # Green
        elif 25.0 <= bmi <= 29.9:
            return "Overweight", "#e67e22" # Dark Orange
        else:
            return "Obese", "#c0392b"      # Red

    def calculate_and_save(self):
        """Validates input, calculates BMI, updates GUI, and logs data to SQLite."""
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Input Error", "Please enter a valid username.")
            return

        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())

            if weight <= 0 or height <= 0:
                raise ValueError("Values must be positive numbers.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for weight and height.")
            return

        # Perform calculation
        bmi = self.calculate_bmi(weight, height)
        category, color_code = self.get_category(bmi)

        # Update GUI labels
        self.bmi_label.config(text=f"BMI: {bmi}")
        self.category_label.config(text=f"Category: {category}", fg=color_code)

        # Save to database
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bmi_history (username, weight, height, bmi, category)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, weight, height, bmi, category))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to save record: {e}")

    def show_trend_chart(self):
        """Fetches user history from database and displays a matplotlib trend graph."""
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Input Error", "Please enter a username to view trends.")
            return

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT date, bmi FROM bmi_history WHERE username = ? ORDER BY date ASC
            ''', (username,))
            rows = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to read from database: {e}")
            return

        if not rows:
            messagebox.showinfo("No Data", f"No historical BMI records found for '{username}'.")
            return

        dates = [row[0] for row in rows]
        bmis = [row[1] for row in rows]

        # Plotting with matplotlib
        plt.figure(figsize=(7, 4))
        plt.plot(dates, bmis, marker='o', linestyle='-', color='#2980b9', linewidth=2)
        plt.axhline(y=18.5, color='orange', linestyle='--', label='Underweight Threshold (18.5)')
        plt.axhline(y=25.0, color='green', linestyle='--', label='Normal Upper Limit (25.0)')
        plt.axhline(y=30.0, color='red', linestyle='--', label='Obese Threshold (30.0)')
        
        plt.title(f"BMI Trend Over Time — {username}")
        plt.xlabel("Date & Time")
        plt.ylabel("BMI Value")
        plt.xticks(rotation=30, ha='right')
        plt.legend(loc='upper left', fontsize='small')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
