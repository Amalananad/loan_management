from django.urls import path
from .views import (
    UserRegisterView,
    LoanListCreateView,
    LoanDetailView,
    LoanRepaymentView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    VerifyOTPView,
    add_loan,
    UserListView,
    LoanForeclosureView,
    LoanListView,
)

urlpatterns = [
    # Auth Routes
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),

    # Loan Routes
    path('loans/', LoanListCreateView.as_view(), name='loan-list-create'),  # Create and list loans
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),  # Retrieve, update, delete a loan
    path('loans/add/', add_loan, name='add_loan'),  # Add a loan
    path('loans/<int:loan_id>/repay/', LoanRepaymentView.as_view(), name='loan-repay'),  # Repay a loan
    path('loans/<int:loan_id>/foreclose/', LoanForeclosureView.as_view(), name='loan-foreclose'),  # Foreclose a loan

    # User Routes
    path('users/', UserListView.as_view(), name='user-list'),  # List users

    # Root API Endpoint
    path('', LoanListView.as_view(), name='loan-list'),  # Default route for loan listing
    path("api/loans/", LoanListCreateView.as_view(), name="loan-list-create"),

]