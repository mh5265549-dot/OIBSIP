import secrets
import string
import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator - Oasis Infobyte")
        self.root.geometry("460x640")
        self.root.resizable(False, False)

        # Session history list (stores up to the last 5 generated passwords)
        self.history = []

        # --- TITLE BANNER (Oasis Infobyte Internship Info) ---
        banner_frame = tk.Frame(root, bg="#2c3e50", pady=8)
        banner_frame.pack(fill="x")
        
        banner_name = tk.Label(banner_frame, text="Hashir Shoaib", font=("Arial", 11, "bold"), fg="white", bg="#2c3e50")
        banner_name.pack()
        
        banner_details = tk.Label(banner_frame, text="Track: Python Programming | Task 3: Password Generator", font=("Arial", 9), fg="#bdc3c7", bg="#2c3e50")
        banner_details.pack()

        # Main Header
        title_label = tk.Label(root, text="Secure Password Generator", font=("Arial", 14, "bold"), fg="#2c3e50")
        title_label.pack(pady=10)

        # --- CONTROLS FRAME ---
        control_frame = tk.LabelFrame(root, text=" Complexity & Criteria ", font=("Arial", 10, "bold"), padx=15, pady=10)
        control_frame.pack(fill="x", padx=20, pady=5)

        # Length Spinbox
        tk.Label(control_frame, text="Password Length (min 8):", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=6)
        self.length_spin = ttk.Spinbox(control_frame, from_=8, to=64, width=5, font=("Arial", 10))
        self.length_spin.set(12)
        self.length_spin.grid(row=0, column=1, sticky="w", pady=6, padx=5)

        # Checkboxes
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.num_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)
        self.ambiguous_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(control_frame, text="Include Uppercase Letters (A-Z)", variable=self.upper_var).grid(row=1, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(control_frame, text="Include Lowercase Letters (a-z)", variable=self.lower_var).grid(row=2, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(control_frame, text="Include Numbers (0-9)", variable=self.num_var).grid(row=3, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(control_frame, text="Include Symbols (!@#$...)", variable=self.symbol_var).grid(row=4, column=0, columnspan=2, sticky="w", pady=2)
        
        # Ambiguous Checkbox
        ttk.Checkbutton(control_frame, text="Exclude Ambiguous Characters (0, O, l, 1)", variable=self.ambiguous_var).grid(row=5, column=0, columnspan=2, sticky="w", pady=(6, 2))

        # --- ACTION BUTTON ---
        generate_btn = tk.Button(root, text="Generate Secure Password", font=("Arial", 10, "bold"), bg="#27ae60", fg="white", padx=15, pady=6, command=self.generate_password)
        generate_btn.pack(pady=12)

        # --- RESULTS FRAME ---
        result_frame = tk.LabelFrame(root, text=" Output & Strength ", font=("Arial", 10, "bold"), padx=15, pady=10)
        result_frame.pack(fill="x", padx=20, pady=5)

        self.password_entry = tk.Entry(result_frame, font=("Courier", 12, "bold"), width=30, justify="center")
        self.password_entry.pack(fill="x", pady=5)

        self.strength_label = tk.Label(result_frame, text="Strength: --", font=("Arial", 10, "bold"), fg="#7f8c8d")
        self.strength_label.pack(anchor="w", pady=2)

        self.clipboard_status = tk.Label(result_frame, text="", font=("Arial", 9, "italic"), fg="#27ae60")
        self.clipboard_status.pack(anchor="w")

        # --- HISTORY FRAME ---
        history_frame = tk.LabelFrame(root, text=" Recent Session History (Last 5) ", font=("Arial", 10, "bold"), padx=15, pady=10)
        history_frame.pack(fill="x", padx=20, pady=5)

        self.history_listbox = tk.Listbox(history_frame, height=5, font=("Courier", 9))
        self.history_listbox.pack(fill="x")

    def generate_password(self):
        """Generates a cryptographically secure password based on user choices and rules."""
        # Validate Length
        try:
            length = int(self.length_spin.get())
            if length < 8:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Password length must be an integer of at least 8 characters.")
            return

        # Validate Character Types
        char_pools = []
        mandatory_chars = []

        upper_chars = string.ascii_uppercase
        lower_chars = string.ascii_lowercase
        num_chars = string.digits
        symbol_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?"

        if self.ambiguous_var.get():
            ambiguous = "0OIl1"
            upper_chars = "".join(c for c in upper_chars if c not in ambiguous)
            lower_chars = "".join(c for c in lower_chars if c not in ambiguous)
            num_chars = "".join(c for c in num_chars if c not in ambiguous)
            symbol_chars = "".join(c for c in symbol_chars if c not in ambiguous)

        if self.upper_var.get():
            if not upper_chars:
                messagebox.showerror("Error", "No uppercase characters available after excluding ambiguous ones.")
                return
            char_pools.append(upper_chars)
            mandatory_chars.append(secrets.choice(upper_chars))

        if self.lower_var.get():
            if not lower_chars:
                messagebox.showerror("Error", "No lowercase characters available after excluding ambiguous ones.")
                return
            char_pools.append(lower_chars)
            mandatory_chars.append(secrets.choice(lower_chars))

        if self.num_var.get():
            if not num_chars:
                messagebox.showerror("Error", "No number characters available after excluding ambiguous ones.")
                return
            char_pools.append(num_chars)
            mandatory_chars.append(secrets.choice(num_chars))

        if self.symbol_var.get():
            if not symbol_chars:
                messagebox.showerror("Error", "No symbol characters available after excluding ambiguous ones.")
                return
            char_pools.append(symbol_chars)
            mandatory_chars.append(secrets.choice(symbol_chars))

        # Enforce at least 2 character types rule
        if len(char_pools) < 2:
            messagebox.showerror("Validation Error", "You must select at least 2 character types.")
            return

        if length < len(mandatory_chars):
            messagebox.showerror("Validation Error", f"Length is too short to include one character from each selected type (minimum {len(mandatory_chars)}).")
            return

        # Combine all selected pools
        combined_pool = "".join(char_pools)

        # Fill remaining characters securely
        remaining_length = length - len(mandatory_chars)
        password_chars = mandatory_chars + [secrets.choice(combined_pool) for _ in range(remaining_length)]
        
        # Shuffle cryptographically securely
        secure_list = list(password_chars)
        secrets.SystemRandom().shuffle(secure_list)
        password = "".join(secure_list)

        # Display result
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

        # Calculate Strength
        strength, color = self.evaluate_strength(password, len(char_pools))
        self.strength_label.config(text=f"Strength: {strength}", fg=color)

        # Auto-copy to clipboard using pyperclip
        try:
            pyperclip.copy(password)
            self.clipboard_status.config(text="Password automatically copied to clipboard!")
        except Exception:
            self.clipboard_status.config(text="Clipboard copy failed.")

        # Update History (Keep last 5)
        self.history.insert(0, password)
        if len(self.history) > 5:
            self.history.pop()

        self.history_listbox.delete(0, tk.END)
        for pwd in self.history:
            self.history_listbox.insert(tk.END, pwd)

    def evaluate_strength(self, password, diversity_count):
        """Evaluates password strength based on length and character type diversity."""
        length = len(password)
        if length >= 14 and diversity_count >= 3:
            return "Strong", "#27ae60"  # Green
        elif length >= 10 and diversity_count >= 2:
            return "Medium", "#e67e22" # Orange
        else:
            return "Weak", "#c0392b"   # Red

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
