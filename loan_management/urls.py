# loan_management/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('loans.urls')),  # ✅ THIS SHOULD BE THE ONLY API PREFIX

  # Include the loans app URLs
]
