import socket

# Operation categories
basic_ops = ['add', 'subtract', 'multiply', 'divide', 'power', 'mod']
single_ops = ['sqrt', 'log', 'ln', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'factorial']
stat_ops = ['mean', 'median', 'mode', 'stddev', 'variance']
trig_ops = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh']

all_ops = set(basic_ops + single_ops + stat_ops)

# Setup UDP client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 12345)

print("🔗 Scientific Calculator with Chained Expression Support (type 'stop' to exit)")
print("Available modes: basic, scientific, statistics, chained")
print("Type 'help' anytime to see available operations.\n")

history = []

def is_valid_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def is_valid_integer(value):
    try:
        return float(value).is_integer()
    except ValueError:
        return False

def list_operations(ops):
    print("\nAvailable operations:")
    for op in ops:
        print(f" - {op}")

while True:
    mode = input("\nEnter mode (basic/scientific/statistics/chained/stop/help): ").strip().lower()

    if mode == 'stop':
        print("Exiting calculator...")
        break

    if mode == 'help':
        print("\nAvailable modes:")
        print(" - basic")
        print(" - scientific")
        print(" - statistics")
        print(" - chained")
        print("Type 'stop' to exit.")
        continue

    if mode == 'chained':
        expr = input("Enter chained expression (e.g., add(2, multiply(3, 4))): ").strip()
        if not expr:
            print("Empty expression.")
            continue
        message = f"chain:{expr}"
        label = expr

    elif mode == 'basic':
        list_operations(basic_ops)
        operation = input("Choose a basic operation: ").strip().lower()
        if operation not in basic_ops:
            print("Unsupported basic operation.")
            continue
        num1 = input("Enter first number: ").strip()
        num2 = input("Enter second number: ").strip()
        if not is_valid_number(num1) or not is_valid_number(num2):
            print("Invalid input(s).")
            continue
        message = f"{operation},{num1},{num2}"
        label = f"{operation}({num1}, {num2})"

    elif mode == 'scientific':
        list_operations(single_ops)
        operation = input("Choose a scientific operation: ").strip().lower()
        if operation not in single_ops:
            print("Unsupported scientific operation.")
            continue
        num1 = input("Enter number: ").strip()
        if not is_valid_number(num1):
            print("Invalid number.")
            continue
        if operation == "factorial":
            if float(num1) < 0 or not is_valid_integer(num1):
                print("Factorial requires a non-negative integer.")
                continue
        message = f"{operation},{num1},0"
        label = f"{operation}({num1})"

    elif mode == 'statistics':
        list_operations(stat_ops)
        operation = input("Choose a statistical operation: ").strip().lower()
        if operation not in stat_ops:
            print("Unsupported statistical operation.")
            continue
        nums = input("Enter numbers (space-separated): ").strip()
        if not nums or not all(is_valid_number(n) for n in nums.split()):
            print("Invalid list of numbers.")
            continue
        message = f"{operation},{nums}"
        label = f"{operation}({nums})"

    else:
        print("Invalid mode.")
        continue

    try:
        client_socket.sendto(message.encode(), server_address)
        result, _ = client_socket.recvfrom(4096)
        result_str = result.decode()
        print(f"Result: {result_str}")
        history.append((label, result_str))
    except Exception as e:
        print(f"Error: {str(e)}")

client_socket.close()

# Print operation history
if history:
    print("\nOperation History:")
    for i, (expr, res) in enumerate(history, 1):
        print(f"  {i}. {expr} = {res}")
else:
    print("No operations performed.")
