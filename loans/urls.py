from django.urls import path
from .views import (
    UserRegisterView, LoanListCreateView, LoanDetailView,
    LoanRepaymentView, CustomTokenObtainPairView, CustomTokenRefreshView,
    VerifyOTPView, add_loan, UserListView, LoanForeclosureView,LoanListView,CustomTokenObtainPairView
    
)
 

urlpatterns = [
    # Auth Routes
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('', LoanListView.as_view(), name='loan-list'),  # ✅ Ensure at least one valid route exists
    path('loans/', LoanListView.as_view(), name='loan-list'),

    # Loan Routes
    path('loans/', LoanListCreateView.as_view(), name='loan-list-create'),
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),
    path('loans/add/', add_loan, name='add_loan'),
    path('loans/<int:loan_id>/repay/', LoanRepaymentView.as_view(), name='loan-repay'),
    path('loans/<int:loan_id>/foreclose/', LoanForeclosureView.as_view(), name='loan-foreclose'),

    # User Routes
    path('users/', UserListView.as_view(), name='user-list'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

]

