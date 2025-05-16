import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Global variables
a = [[0 for _ in range(100)] for _ in range(100)]
b = [0] * 100
B = [0] * 100
c = [0] * 100
mp = [{} for _ in range(100)]
m, n = 0, 0
s = [""] * 100

def display():
    """Display the matrix for debugging"""
    print()
    for i in range(m):
        for j in range(n):
            print(a[i][j], end=" ")
        print()
    print()

def int_to_string(n):
    """Convert integer to string"""
    if n == 0:
        return "0"
    return str(n)

def gcd(a, b):
    """Find greatest common divisor"""
    if a == 0 and b == 0:
        return 0
    if a * b == 0:
        return b if a == 0 else a
    while a % b != 0:
        d = a % b
        a = b
        b = d
    return b

def swap_rows(l, r):
    """Swap two rows in matrix"""
    for j in range(n):
        a[l][j], a[r][j] = a[r][j], a[l][j]

def multiply_row(i, k):
    """Multiply a row by a constant"""
    for j in range(n):
        a[i][j] *= k

def subtract_rows(i1, i2):
    """Subtract row i2 from row i1"""
    for j in range(n):
        a[i1][j] -= a[i2][j]

def parse_compound(compound, V):
    """Parse a chemical compound and update the mp dictionary"""
    global mp
    
    i = 0
    while i < len(compound):
        if 'A' <= compound[i] <= 'Z':
            # Start of an element symbol
            element = compound[i]
            i += 1
            
            # Read lowercase letters (rest of element symbol)
            while i < len(compound) and 'a' <= compound[i] <= 'z':
                element += compound[i]
                i += 1
            
            # Check for coefficient (number after element)
            coef = 1
            if i < len(compound) and '0' <= compound[i] <= '9':
                coef_str = ""
                while i < len(compound) and '0' <= compound[i] <= '9':
                    coef_str += compound[i]
                    i += 1
                coef = int(coef_str)
            
            # Add element to dictionary
            if element not in mp[V]:
                mp[V][element] = 0
            mp[V][element] += coef * b[V]
            
        elif compound[i] == '(':
            # Find matching closing parenthesis
            paren_depth = 1
            start = i + 1
            i += 1
            
            while i < len(compound) and paren_depth > 0:
                if compound[i] == '(':
                    paren_depth += 1
                elif compound[i] == ')':
                    paren_depth -= 1
                i += 1
            
            if paren_depth != 0:
                raise ValueError(f"Mismatched parentheses in compound: {compound}")
            
            end = i - 1  # Position of closing parenthesis
            
            # Check for coefficient after parentheses
            coef = 1
            if i < len(compound) and '0' <= compound[i] <= '9':
                coef_str = ""
                while i < len(compound) and '0' <= compound[i] <= '9':
                    coef_str += compound[i]
                    i += 1
                coef = int(coef_str)
            
            # Parse the content inside parentheses with the coefficient
            inside = compound[start:end]
            
            # Temporarily store current mp[V]
            old_mp = mp[V].copy()
            
            # Parse the content inside parentheses
            temp_mp = {}
            parse_group(inside, temp_mp)
            
            # Apply the coefficient and add to mp[V]
            for element, count in temp_mp.items():
                if element not in mp[V]:
                    mp[V][element] = 0
                mp[V][element] += count * coef * b[V]
            
        else:
            # Skip other characters (like spaces)
            i += 1

def parse_group(group, result_mp):
    """Parse a group (inside parentheses) and update the provided dict"""
    i = 0
    while i < len(group):
        if 'A' <= group[i] <= 'Z':
            # Start of an element symbol
            element = group[i]
            i += 1
            
            # Read lowercase letters (rest of element symbol)
            while i < len(group) and 'a' <= group[i] <= 'z':
                element += group[i]
                i += 1
            
            # Check for coefficient (number after element)
            coef = 1
            if i < len(group) and '0' <= group[i] <= '9':
                coef_str = ""
                while i < len(group) and '0' <= group[i] <= '9':
                    coef_str += group[i]
                    i += 1
                coef = int(coef_str)
            
            # Add element to dictionary
            if element not in result_mp:
                result_mp[element] = 0
            result_mp[element] += coef
            
        elif group[i] == '(':
            # Handle nested parentheses (recursive call)
            paren_depth = 1
            start = i + 1
            i += 1
            
            while i < len(group) and paren_depth > 0:
                if group[i] == '(':
                    paren_depth += 1
                elif group[i] == ')':
                    paren_depth -= 1
                i += 1
            
            if paren_depth != 0:
                raise ValueError(f"Mismatched parentheses in group: {group}")
            
            end = i - 1  # Position of closing parenthesis
            
            # Check for coefficient after parentheses
            coef = 1
            if i < len(group) and '0' <= group[i] <= '9':
                coef_str = ""
                while i < len(group) and '0' <= group[i] <= '9':
                    coef_str += group[i]
                    i += 1
                coef = int(coef_str)
            
            # Parse the content inside nested parentheses
            inside = group[start:end]
            
            # Temporarily store current mp
            temp_mp = {}
            parse_group(inside, temp_mp)
            
            # Apply the coefficient and add to result_mp
            for element, count in temp_mp.items():
                if element not in result_mp:
                    result_mp[element] = 0
                result_mp[element] += count * coef
            
        else:
            # Skip other characters
            i += 1

def matrix(equation_str):
    """Parse the chemical equation into a matrix"""
    global m, n, mp
    
    equation_str = equation_str + "+"
    n = 0
    k = 1
    current_compound = ""
    
    # Parse equation into compounds
    i = 0
    while i < len(equation_str):
        if equation_str[i] == ' ':
            i += 1
            continue
        if equation_str[i] == '+':
            b[n] = k
            s[n] = current_compound
            n += 1
            current_compound = ""
            i += 1
        elif equation_str[i] == '=':
            b[n] = k
            s[n] = current_compound
            n += 1
            current_compound = ""
            k = -1
            i += 1
        else:
            current_compound += equation_str[i]
            i += 1
    
    # Copy b to B
    for i in range(n):
        B[i] = b[i]
    
    # Reset mp dictionaries
    for i in range(n):
        mp[i] = {}
    
    # Parse each compound for elements using the new parser
    for V in range(n):
        parse_compound(s[V], V)
    
    # Build the coefficient matrix
    m = 0
    M = {}
    
    for V in range(n):
        for element in mp[V]:
            if element not in M:
                M[element] = True
                for j in range(n):
                    a[m][j] = mp[j].get(element, 0)
                m += 1

def simplify():
    """Simplify each row in the matrix by dividing by GCD"""
    for i in range(m):
        # Find first non-zero element in row
        row_gcd = 0
        for j in range(n):
            if a[i][j] != 0:
                row_gcd = a[i][j]
                break
        
        # Find GCD of all elements in row
        for j in range(n):
            if a[i][j] != 0:
                row_gcd = gcd(row_gcd, a[i][j])
        
        # Divide row by GCD
        if row_gcd != 0:
            for j in range(n):
                a[i][j] //= row_gcd

def solve():
    """Solve the system of equations using Gaussian elimination"""
    global m  # Declare m as global variable
    
    # Forward elimination
    for v in range(n - 1):
        k = m - 1
        while k >= 0 and a[k][v] == 0:
            k -= 1
        
        if k < 0:  # Skip if column is all zeros
            continue
            
        for i in range(k - 1, v - 1, -1):
            if i < 0:
                break
            if a[i][v] == 0:
                swap_rows(i, k)
                k -= 1
        
        for i in range(m - 1, v, -1):
            if a[i][v] != 0 and a[v][v] != 0:
                t = a[v][v]
                multiply_row(v, a[i][v])
                multiply_row(i, t)
                subtract_rows(i, v)
        
        simplify()
    
    m = n - 1  # Update global m
    
    # Back substitution
    for v in range(n - 2, 0, -1):
        for i in range(v):
            if a[i][v] != 0 and a[v][v] != 0:
                t = a[v][v]
                multiply_row(v, a[i][v])
                multiply_row(i, t)
                subtract_rows(i, v)
        
        simplify()
    
    # Calculate coefficients
    c[n - 1] = 1
    for i in range(n - 1):
        if a[i][i] != 0:  # Avoid division by zero
            c[n - 1] *= a[i][i]
    
    for i in range(n - 1):
        if a[i][i] != 0:  # Avoid division by zero
            c[i] = -c[n - 1] * a[i][n - 1] // a[i][i]
        else:
            c[i] = 1  # Default to 1 if division by zero would occur
    
    # Take absolute values
    for i in range(n):
        if c[i] < 0:
            c[i] = -c[i]
    
    # Find GCD of all coefficients to simplify
    k = c[0]
    for i in range(1, n):
        k = gcd(k, c[i])
    
    # Divide all coefficients by GCD
    if k > 0:
        for i in range(n):
            c[i] //= k

def pthh(equation_str):
    """Process a chemical equation and return the balanced version"""
    global m, n, mp
    
    # Reset variables for new equation
    for i in range(100):
        mp[i] = {}
        for j in range(100):
            a[i][j] = 0
    
    matrix(equation_str)
    solve()
    
    result = ""
    
    # First compound
    if c[0] > 1:
        result += str(c[0])
    result += s[0]
    
    # Remaining compounds
    for i in range(1, n):
        if B[i] > 0:
            result += " + "
            if c[i] > 1:
                result += int_to_string(c[i])
            result += s[i]
        else:
            if B[i-1] > 0:
                result += " → "  # Using arrow instead of equals sign
            if c[i] > 1:
                result += int_to_string(c[i])
            result += s[i]
            if i != n - 1:
                result += " + "
    
    return result

# GUI Class
class ChemicalEquationBalancerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chemical Equation Balancer")
        self.root.geometry("800x600")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Configure style
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10))
        style.configure("TLabel", font=("Arial", 11))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="Chemical Equation Balancer", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding=10)
        input_frame.pack(fill=tk.X, pady=10)
        
        instruction_label = ttk.Label(input_frame, 
                                     text="Enter a chemical equation (e.g., AlP + HNO3 = H3PO4 + Al(NO3)3 + N2O + H2O)")
        instruction_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Input entry with larger font
        self.equation_var = tk.StringVar()
        self.equation_entry = ttk.Entry(input_frame, 
                                       textvariable=self.equation_var, 
                                       font=("Arial", 12), 
                                       width=50)
        self.equation_entry.pack(fill=tk.X, pady=5)
        self.equation_entry.focus()
        
        # Buttons frame
        buttons_frame = ttk.Frame(input_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        balance_button = ttk.Button(buttons_frame, 
                                   text="Balance Equation", 
                                   command=self.balance)
        balance_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(buttons_frame, 
                                 text="Clear", 
                                 command=self.clear_input)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Balanced Equation", padding=10)
        output_frame.pack(fill=tk.X, pady=10)
        
        self.result_var = tk.StringVar()
        self.result_var.set("")
        result_label = ttk.Label(output_frame, 
                                textvariable=self.result_var, 
                                font=("Arial", 12, "bold"))
        result_label.pack(fill=tk.X, pady=10)
        
        # History section
        history_frame = ttk.LabelFrame(main_frame, text="History", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.history_text = scrolledtext.ScrolledText(history_frame, 
                                                    font=("Arial", 11),
                                                    wrap=tk.WORD)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Bottom buttons
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=10)
        
        clear_history_btn = ttk.Button(bottom_frame, 
                                      text="Clear History", 
                                      command=self.clear_history)
        clear_history_btn.pack(side=tk.LEFT, padx=5)
        
        exit_btn = ttk.Button(bottom_frame, 
                             text="Exit", 
                             command=self.root.destroy)
        exit_btn.pack(side=tk.RIGHT, padx=5)
        
    def balance(self):
        equation = self.equation_var.get().strip()
        
        if not equation:
            messagebox.showwarning("Input Error", "Please enter a chemical equation.")
            return
        
        try:
            result = pthh(equation)
            self.result_var.set(result)
            
            # Add to history
            history_entry = f"Input: {equation}\nBalanced: {result}\n{'-'*50}\n"
            self.history_text.insert(tk.END, history_entry)
            self.history_text.see(tk.END)  # Scroll to the end
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while balancing the equation: {str(e)}")
    
    def clear_input(self):
        self.equation_var.set("")
        self.result_var.set("")
        self.equation_entry.focus()
    
    def clear_history(self):
        self.history_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = ChemicalEquationBalancerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()