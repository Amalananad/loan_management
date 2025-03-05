# loan_management/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('loans.urls')),
    path('api/', include('loans.urls')),  # ✅ Make sure this is correct

    path("api/loans/", include("loans.urls")),  # Ensure it's correctly included
  # Include the loans app URLs
]
