transactions = []
balance = 0.0

def add_transaction(date, t_type, category, amount):
    global balance
    transaction = {
        "date": date,
        "type": t_type,
        "category": category,
        "amount": amount
    }
    transactions.append(transaction)
    if t_type == 'income':
        balance += amount
    elif t_type == 'expense':
        balance -= amount
