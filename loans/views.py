from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_otp.plugins.otp_email.models import EmailDevice
from django.contrib.auth.models import User
from .models import Loan  # Ensure only one Loan model is used
from .serializers import UserSerializer, LoanSerializer
from rest_framework.views import APIView
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class LoanListView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
# ✅ Loan Repayment View
class LoanRepaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, loan_id):
        try:
            loan = Loan.objects.get(id=loan_id, user=request.user)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found."}, status=status.HTTP_404_NOT_FOUND)

        amount = request.data.get("amount")

        if not amount:
            return Response({"error": "Amount is required."}, status=status.HTTP_400_BAD_REQUEST)

        amount = Decimal(str(amount))

        if amount < loan.monthly_installment:
            return Response({"error": "Amount is less than the required installment."}, status=status.HTTP_400_BAD_REQUEST)

        loan.amount_paid += amount
        loan.save()

        return Response({"message": "Installment paid successfully!"}, status=status.HTTP_200_OK)


# ✅ User Registration View
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# ✅ User List View
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Loan List & Create View
class LoanListCreateView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        loan = serializer.save(user=self.request.user)
        response_data = {
            "status": "success",
            "data": {
                "loan_id": loan.id,
                "amount": loan.amount,
                "tenure": loan.tenure,
                "interest_rate": f"{loan.interest_rate}% yearly",
                "monthly_installment": loan.calculate_monthly_installment(),
                "total_interest": loan.calculate_total_interest(),
                "total_amount": loan.calculate_total_payable(),
                "payment_schedule": loan.generate_payment_schedule()
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

# ✅ Loan Detail View
class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

# ✅ Loan Foreclosure View
class LoanForeclosureView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, loan_id):
        logger.info(f"Received foreclosure request for loan_id: {loan_id}")

        try:
            loan = Loan.objects.get(id=loan_id)
        except Loan.DoesNotExist:
            logger.error(f"Loan ID {loan_id} not found.")
            return Response({"error": "Loan not found."}, status=status.HTTP_404_NOT_FOUND)

        logger.info(f"Foreclosing loan {loan_id}...")

        # Calculate the total amount payable
        total_amount = Decimal(str(loan.calculate_total_payable()))  # Ensure total_amount is Decimal
        foreclosure_discount = round(total_amount * Decimal("0.05"), 2)
        final_settlement_amount = round(total_amount - foreclosure_discount, 2)



        # Update loan status
        loan.status = "CLOSED"
        loan.save()

        return Response({
            "status": "success",
            "message": "Loan foreclosed successfully.",
            "data": {
                "loan_id": loan.id,
                "amount_paid": float(loan.amount_paid),
                "foreclosure_discount": float(foreclosure_discount),
                "final_settlement_amount": float(final_settlement_amount),
                "status": "CLOSED"
            }
        }, status=status.HTTP_200_OK)

# ✅ Custom Token Views
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]

# ✅ OTP Verification View
class VerifyOTPView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            user = User.objects.get(email=email)
            device = EmailDevice.objects.get(user=user, key=otp)
            device.confirm()
            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except EmailDevice.DoesNotExist:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

# ✅ Add Loan API View
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_loan(request):
    amount = request.data.get('amount')
    tenure = request.data.get('tenure')
    interest_rate = request.data.get('interest_rate')
    user = request.user  

    try:
        loan = Loan.objects.create(
            user=user, amount=amount, tenure=tenure, interest_rate=interest_rate
        )
        return Response({
            "status": "success",
            "data": {
                "loan_id": loan.id,
                "amount": amount,
                "tenure": tenure,
                "interest_rate": f"{interest_rate}% yearly",
                "monthly_installment": loan.calculate_monthly_installment(),
                "total_interest": loan.calculate_total_interest(),
                "total_amount": loan.calculate_total_payable(),
                "payment_schedule": loan.generate_payment_schedule()
            }
        }, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
