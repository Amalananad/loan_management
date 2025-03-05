from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from decimal import Decimal

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()  # in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # yearly interest rate
    loan_type = models.CharField(max_length=50, blank=True, null=True)  # Optional field
    purpose = models.CharField(max_length=255, blank=True, null=True)  # Optional field
    collateral = models.CharField(max_length=255, blank=True, null=True)  # Optional field
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_loan_id(self):
        return f"LOAN{self.id:03d}"  # Example: LOAN001

    def calculate_monthly_installment(self):
        """
        Calculates the monthly installment using the annuity formula.
        """
        principal = float(self.amount)
        annual_rate = float(self.interest_rate) / 100
        monthly_rate = annual_rate / 12  
        n_payments = self.tenure  

        if monthly_rate > 0:
            installment = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -n_payments)
        else:
            installment = principal / n_payments  # If interest rate is 0

        return round(installment, 2)

    def calculate_total_payable(self):
        """Total amount payable over the tenure."""
        return round(self.calculate_monthly_installment() * self.tenure, 2)

    def calculate_total_interest(self):
        """✅ FIX: Convert values to `Decimal` to prevent TypeError"""
        total_payable = Decimal(self.calculate_total_payable())  # Convert to Decimal
        return total_payable - self.amount  # Both values are now Decimal

    def generate_payment_schedule(self):
        """
        Generates a monthly payment schedule including due dates.
        """
        schedule = []
        monthly_installment = self.calculate_monthly_installment()
        for i in range(1, self.tenure + 1):
            due_date = self.created_at + timedelta(days=30 * i)  
            schedule.append({
                "installment_no": i,
                "due_date": due_date.strftime("%Y-%m-%d"),
                "amount": monthly_installment
            })
        return schedule
