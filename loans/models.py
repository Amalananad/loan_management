from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from decimal import Decimal

class Loan(models.Model):
    # ✅ Define STATUS_CHOICES before using it
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('CLOSED', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()  # in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # yearly interest rate
    loan_id = models.CharField(max_length=20, unique=True, blank=True)  # Ensure this field is unique
    loan_type = models.CharField(max_length=50, blank=True, null=True)  # Optional field
    purpose = models.CharField(max_length=255, blank=True, null=True)  # Optional field
    collateral = models.CharField(max_length=255, blank=True, null=True)  # Optional field
    created_at = models.DateTimeField(auto_now_add=True)
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Add this field
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')  # ✅ Now it works!

    def save(self, *args, **kwargs):
        """Generate Loan ID and Monthly Installment before saving."""
        if not self.loan_id:  # Generate loan_id only if it doesn't exist
            super().save(*args, **kwargs)  # Save first to get `pk`
            self.loan_id = self.generate_loan_id()
            self.monthly_installment = self.calculate_monthly_installment()  # Calculate EMI
            self.save(update_fields=['loan_id', 'monthly_installment'])  # Save changes after initial save
        else:
            super().save(*args, **kwargs)

    def generate_loan_id(self):
        """Generate Loan ID using Loan PK"""
        return f"LOAN{self.pk:03d}"

    def calculate_monthly_installment(self):
        """Calculates the monthly installment using the annuity formula."""
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
        """Calculates total interest payable."""
        total_payable = Decimal(self.calculate_total_payable())  # Convert to Decimal
        return total_payable - self.amount  # Both values are now Decimal

    def generate_payment_schedule(self):
        """Generates a monthly payment schedule including due dates."""
        schedule = []
        monthly_installment = self.calculate_monthly_installment()
        for i in range(1, self.tenure + 1):
            due_date = self.created_at.date() + timedelta(days=30 * i)  # Use .date() to avoid errors
            schedule.append({
                "installment_no": i,
                "due_date": due_date.strftime("%Y-%m-%d"),
                "amount": monthly_installment
            })
        return schedule
