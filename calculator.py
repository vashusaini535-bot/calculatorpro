
import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import math

# ---------------- MATH ENGINE ----------------

x, y = sp.symbols('x y')

def solve_math(expression):
    try:
        expr = expression.strip()

        # Linear equation
        if "=" in expr:
            left, right = expr.split("=", 1)
            equation = sp.Eq(
                sp.sympify(left),
                sp.sympify(right)
            )
            variables = list(equation.free_symbols)

            if len(variables) == 1:
                return "Solution:\n" + str(
                    sp.solve(equation, variables[0])
                )

            return "Solution:\n" + str(
                sp.solve(equation, variables)
            )

        # Algebraic expression
        result = sp.sympify(expr)

        return (
            "Simplified:\n" + str(sp.simplify(result))
            + "\n\nFactorised:\n" + str(sp.factor(result))
            + "\n\nExpanded:\n" + str(sp.expand(result))
        )

    except Exception as e:
        return "Invalid expression!\n" + str(e)


# ---------------- CALCULATOR GUI ----------------

root = tk.Tk()
root.title("ADVANCED MATH CALCULATOR")
root.geometry("950x680")
root.configure(bg="#101827")
root.minsize(750, 550)

# Colors
BG = "#101827"
PANEL = "#1e293b"
ACCENT = "#38bdf8"
WHITE = "#f8fafc"
GREEN = "#22c55e"

# Heading
title = tk.Label(
    root,
    text="ADVANCED MATH CALCULATOR",
    font=("Arial", 25, "bold"),
    bg=BG,
    fg=ACCENT
)
title.pack(pady=15)

subtitle = tk.Label(
    root,
    text="CLASS 10 MATHEMATICS SOLVER",
    font=("Arial", 11),
    bg=BG,
    fg="white"
)
subtitle.pack()

# Main frame
main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=25, pady=20)

# Left calculator panel
left = tk.Frame(main, bg=PANEL, padx=15, pady=15)
left.pack(side="left", fill="both", expand=True)

tk.Label(
    left,
    text="Enter Equation / Expression",
    font=("Arial", 13, "bold"),
    bg=PANEL,
    fg=WHITE
).pack(anchor="w", pady=10)

entry = tk.Entry(
    left,
    font=("Arial", 20),
    bg="#0f172a",
    fg=GREEN,
    insertbackground="white",
    relief="flat"
)
entry.pack(fill="x", ipady=15, pady=10)

# Buttons
buttons = [
    ["7", "8", "9", "/", "sin("],
    ["4", "5", "6", "*", "cos("],
    ["1", "2", "3", "-", "tan("],
    ["0", ".", "^", "+", "sqrt("],
    ["(", ")", "x", "=", "pi"]
]

def insert(value):
    if value == "^":
        value = "**"
    entry.insert(tk.END, value)

button_frame = tk.Frame(left, bg=PANEL)
button_frame.pack(fill="x", pady=15)

for r, row in enumerate(buttons):
    for c, value in enumerate(row):
        btn = tk.Button(
            button_frame,
            text=value,
            font=("Arial", 13, "bold"),
            bg="#334155",
            fg=WHITE,
            activebackground=ACCENT,
            relief="flat",
            command=lambda v=value: insert(v)
        )
        btn.grid(
            row=r,
            column=c,
            padx=4,
            pady=5,
            sticky="nsew",
            ipadx=7,
            ipady=12
        )

for i in range(5):
    button_frame.columnconfigure(i, weight=1)

# Action functions
def calculate():
    expression = entry.get()
    result = solve_math(expression)
    output.delete("1.0", tk.END)
    output.insert(tk.END, result)

def clear():
    entry.delete(0, tk.END)
    output.delete("1.0", tk.END)

def quadratic():
    try:
        a = float(a_entry.get())
        b = float(b_entry.get())
        c = float(c_entry.get())

        equation = a*x**2 + b*x + c

        result = sp.solve(equation, x)
        discriminant = b**2 - 4*a*c

        output.delete("1.0", tk.END)
        output.insert(
            tk.END,
            f"Equation: {equation} = 0\n\n"
            f"Discriminant: {discriminant}\n\n"
            f"Roots: {result}\n\n"
            f"Factorisation: {sp.factor(equation)}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Calculate and clear
tk.Button(
    left,
    text="SOLVE MATHEMATICS",
    font=("Arial", 15, "bold"),
    bg=GREEN,
    fg="#052e16",
    relief="flat",
    command=calculate
).pack(fill="x", pady=8, ipady=10)

tk.Button(
    left,
    text="CLEAR ALL",
    font=("Arial", 12, "bold"),
    bg="#ef4444",
    fg="white",
    relief="flat",
    command=clear
).pack(fill="x", pady=5, ipady=8)

# Right output panel
right = tk.Frame(main, bg=PANEL, padx=15, pady=15)
right.pack(side="right", fill="both", expand=True, padx=(15, 0))

tk.Label(
    right,
    text="SOLUTION & ANSWERS",
    font=("Arial", 16, "bold"),
    bg=PANEL,
    fg=ACCENT
).pack(anchor="w", pady=10)

output = tk.Text(
    right,
    font=("Consolas", 12),
    bg="#0f172a",
    fg=GREEN,
    insertbackground="white",
    relief="flat",
    wrap="word"
)
output.pack(fill="both", expand=True)

# Quadratic solver
tk.Label(
    right,
    text="QUADRATIC EQUATION SOLVER",
    font=("Arial", 12, "bold"),
    bg=PANEL,
    fg=WHITE
).pack(pady=12)

a_entry = tk.Entry(right, font=("Arial", 12))
b_entry = tk.Entry(right, font=("Arial", 12))
c_entry = tk.Entry(right, font=("Arial", 12))

for label, widget in [
    ("Coefficient a:", a_entry),
    ("Coefficient b:", b_entry),
    ("Coefficient c:", c_entry)
]:
    tk.Label(
        right, text=label,
        bg=PANEL, fg=WHITE
    ).pack(anchor="w")
    widget.pack(fill="x", pady=3)

tk.Button(
    right,
    text="SOLVE QUADRATIC",
    bg=ACCENT,
    fg="#082f49",
    font=("Arial", 12, "bold"),
    relief="flat",
    command=quadratic
).pack(fill="x", pady=12, ipady=8)

# Footer
tk.Label(
    root,
    text="Designed for Class 10 Mathematics | Python + SymPy",
    bg=BG,
    fg="#94a3b8",
    font=("Arial", 10)
).pack(pady=10)

root.mainloop()
