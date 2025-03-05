# utils.py

def calculate_loan_details(amount, tenure, interest_rate):
    if amount < 1000 or amount > 100000:
        raise ValueError("Amount must be between ₹1,000 and ₹100,000.")
    if tenure < 3 or tenure > 24:
        raise ValueError("Tenure must be between 3 and 24 months.")
    
    monthly_interest_rate = interest_rate / 12 / 100
    total_interest = amount * monthly_interest_rate * tenure
    total_amount = amount + total_interest
    monthly_installment = total_amount / tenure
    
    return {
        "total_interest": round(total_interest, 2),
        "total_amount": round(total_amount, 2),
        "monthly_installment": round(monthly_installment, 2)
    }