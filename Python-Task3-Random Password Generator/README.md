# Oasis Infobyte Python Development Internship

## Task 3: Advanced Password Generator

A Python-based graphical user interface (GUI) application designed to generate cryptographically secure passwords based on user-defined criteria, strength validation, exclusion rules, and automated clipboard copying.

### Features & Functionality
- **Interactive GUI:** Built using `tkinter` with spinboxes and checkboxes for precise customization.
- **Cryptographically Secure:** Utilizes Python's native `secrets` module instead of `random` to generate secure tokens.
- **Security Rule Enforcement:** Automatically guarantees inclusion of at least one character from every chosen category and enforces a minimum length threshold.
- **Strength Indicator:** Visually rates generated passwords (Weak, Medium, Strong) based on overall character count and type diversity.
- **Clipboard Integration:** Automatically copies the newly generated password to the system clipboard via `pyperclip`.
- **Ambiguous Character Filtering:** Option to omit confusing characters (`0`, `O`, `l`, `1`).
- **Session History:** Dynamically maintains a non-persistent log of the last 5 generated passwords.

---

### Tech Stack
- **Language:** Python 3.x
- **Libraries:** 
  - `tkinter` (GUI framework)
  - `secrets` (Cryptographically secure random number generation)
  - `pyperclip` (Clipboard management)
  - `string` (Character set definitions)

---

### Setup and Installation Instructions

1. **Navigate to the task directory:**
   ```bash
   cd Python-Task3-PasswordGenerator
