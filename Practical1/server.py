import socket
import math
import statistics

# ================================
# 🔢 1. BASIC ARITHMETIC OPERATIONS
# ================================
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b): return a / b if b != 0 else "Error: Division by zero"
def power(a, b): return math.pow(a, b)
def mod(a, b): return a % b

# ================================
# 🧮 2. SCIENTIFIC OPERATIONS
# ================================
def sqrt(a): return math.sqrt(a)
def log(a): return math.log10(a)
def ln(a): return math.log(a)
def exp(a): return math.exp(a)
def factorial(a): return math.factorial(int(a)) if a >= 0 and a.is_integer() else "Error: Invalid input for factorial"

# ================================
# 📐 3. TRIGONOMETRIC OPERATIONS
# ================================
def sin(a): return math.sin(math.radians(a))
def cos(a): return math.cos(math.radians(a))
def tan(a): return math.tan(math.radians(a))
def asin(a): return math.degrees(math.asin(a))
def acos(a): return math.degrees(math.acos(a))
def atan(a): return math.degrees(math.atan(a))
def sinh(a): return math.sinh(a)
def cosh(a): return math.cosh(a)
def tanh(a): return math.tanh(a)

# ================================
# 📊 4. STATISTICAL OPERATIONS
# ================================
def mean(data): return statistics.mean(data)
def median(data): return statistics.median(data)
def mode(data): 
    try:
        return statistics.mode(data)
    except statistics.StatisticsError:
        return "Error: No unique mode"
def stddev(data): return statistics.stdev(data) if len(data) > 1 else "Error: Need ≥ 2 values"
def variance(data): return statistics.variance(data) if len(data) > 1 else "Error: Need ≥ 2 values"

# ================================
# 🔐 SAFE FUNCTION MAP FOR EVAL
# ================================
safe_functions = {
    # Basic
    'add': add, 'subtract': subtract, 'multiply': multiply, 'divide': divide,
    'power': power, 'mod': mod,

    # Scientific
    'sqrt': sqrt, 'log': log, 'ln': ln, 'exp': exp, 'factorial': factorial,

    # Trigonometric
    'sin': sin, 'cos': cos, 'tan': tan,
    'asin': asin, 'acos': acos, 'atan': atan,
    'sinh': sinh, 'cosh': cosh, 'tanh': tanh,

    # Statistics
    'mean': mean, 'median': median, 'mode': mode,
    'stddev': stddev, 'variance': variance
}

# ================================
# 🔧 UDP SERVER SETUP
# ================================
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 12345))
print("📡 UDP Scientific Calculator Server started...")

# ================================
# 🔁 MAIN SERVER LOOP
# ================================
while True:
    message, client_address = server_socket.recvfrom(4096)
    decoded = message.decode()
    print(f"Received from {client_address}: {decoded}")

    try:
        if decoded.startswith("chain:"):
            expr = decoded[6:].strip()
            result = eval(expr, {"__builtins__": None}, safe_functions)
        else:
            parts = decoded.split(',')
            op = parts[0]

            if op in ['mean', 'median', 'mode', 'stddev', 'variance']:
                data = [float(x) for x in parts[1].split()]
                result = safe_functions[op](data)
            elif op in ['sqrt', 'log', 'ln', 'exp', 'sin', 'cos', 'tan',
                        'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'factorial']:
                a = float(parts[1])
                result = safe_functions[op](a)
            else:
                a, b = float(parts[1]), float(parts[2])
                result = safe_functions[op](a, b)

    except Exception as e:
        result = f"Error: {str(e)}"

    server_socket.sendto(str(result).encode(), client_address)
    print(f"Sent to {client_address}: {result}")
