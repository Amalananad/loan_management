from django.urls import path
from .views import (
    UserRegisterView, LoanListCreateView, LoanDetailView, 
    CustomTokenObtainPairView, CustomTokenRefreshView, VerifyOTPView, add_loan,UserListView
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('api/register/', UserRegisterView.as_view(), name='user-register'),
    path('loans/', LoanListCreateView.as_view(), name='loan-list-create'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/loans/', LoanListCreateView.as_view(), name='loan-list-create'),
    path('api/loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),
    path('api/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('api/add-loan/', add_loan, name='add_loan')  ,# Changed to avoid conflict
    path('users/', UserListView.as_view(), name='user-list'),

]
