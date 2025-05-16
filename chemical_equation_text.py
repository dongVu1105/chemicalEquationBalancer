import sys

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
    
    # Parse each compound for elements
    for V in range(n):
        compound = s[V]
        k = 1
        i = len(compound) - 1
        
        while i >= 0:
            # Digit (coefficient)
            if '0' <= compound[i] <= '9':
                if k == 1 and '(' in compound:
                    k = int(compound[i])
                else:
                    t = 1
                    k2 = 0
                    # Parse multi-digit number
                    while i >= 0 and '0' <= compound[i] <= '9':
                        k2 += t * int(compound[i])
                        t *= 10
                        i -= 1
                    
                    # Parse element name
                    element = ""
                    while i >= 0 and 'a' <= compound[i] <= 'z':
                        element = compound[i] + element
                        i -= 1
                    
                    element = compound[i] + element
                    i -= 1
                    
                    # Add to dictionary
                    if element not in mp[V]:
                        mp[V][element] = 0
                    mp[V][element] += k * k2 * b[V]
                    element = ""
            # Lowercase letter (part of element name)
            elif 'a' <= compound[i] <= 'z':
                element = ""
                while i >= 0 and 'a' <= compound[i] <= 'z':
                    element = compound[i] + element
                    i -= 1
                
                element = compound[i] + element
                i -= 1
                
                if element not in mp[V]:
                    mp[V][element] = 0
                mp[V][element] += k * b[V]
                element = ""
            # Uppercase letter (element symbol)
            elif 'A' <= compound[i] <= 'Z':
                element = compound[i]
                i -= 1
                
                if element not in mp[V]:
                    mp[V][element] = 0
                mp[V][element] = k * b[V]
                element = ""
            # Opening parenthesis
            elif compound[i] == '(':
                k = 1
                i -= 1
            else:
                i -= 1
    
    # Build the coefficient matrix
    m = 0
    M = {}
    
    for V in range(n):
        for element in mp[V]:
            if element not in M:
                for j in range(n):
                    a[m][j] = mp[j].get(element, 0)
                m += 1
                M[element] = 123

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
    global m  # Khai báo m là biến toàn cục
    
    # Forward elimination
    for v in range(n - 1):
        k = m - 1
        while a[k][v] == 0:
            k -= 1
        
        for i in range(k - 1, v - 1, -1):
            if a[i][v] == 0:
                swap_rows(i, k)
                k -= 1
        
        for i in range(m - 1, v, -1):
            if a[i][v] != 0:
                t = a[v][v]
                multiply_row(v, a[i][v])
                multiply_row(i, t)
                subtract_rows(i, v)
        
        simplify()
    
    m = n - 1  # Sửa biến toàn cục m
    
    # Back substitution
    for v in range(n - 2, 0, -1):
        for i in range(v):
            if a[i][v] != 0:
                t = a[v][v]
                multiply_row(v, a[i][v])
                multiply_row(i, t)
                subtract_rows(i, v)
        
        simplify()
    
    # Calculate coefficients
    c[n - 1] = 1
    for i in range(n - 1):
        c[n - 1] *= a[i][i]
    
    for i in range(n - 1):
        c[i] = -c[n - 1] * a[i][n - 1] // a[i][i]
    
    # Take absolute values
    for i in range(n):
        if c[i] < 0:
            c[i] = -c[i]
    
    # Find GCD of all coefficients to simplify
    k = c[0]
    for i in range(1, n):
        k = gcd(k, c[i])
    
    # Divide all coefficients by GCD
    for i in range(n):
        c[i] //= k

def pthh(equation_str):
    """Process a chemical equation and return the balanced version"""
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
                result += " = "
            if c[i] > 1:
                result += int_to_string(c[i])
            result += s[i]
            if i != n - 1:
                result += " + "
    
    return result

def main():
    print()
    equation = input()
    balanced = pthh(equation)
    print(balanced)
    print("\n ")

if __name__ == "__main__":
    main()