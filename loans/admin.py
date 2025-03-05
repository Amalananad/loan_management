from django.contrib import admin  # Import Django's admin module
from .models import Loan  # Import your models

admin.site.register(Loan)  # Register your model correctly
