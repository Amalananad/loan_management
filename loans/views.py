from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_otp.plugins.otp_email.models import EmailDevice
from django.contrib.auth.models import User
from .models import Loan  # Ensure only one Loan model is used
from .serializers import UserSerializer, LoanSerializer

# ✅ User Registration View
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        loan = serializer.save(user=self.request.user)  # Assign logged-in user
        response_data = {
            "status": "success",
            "data": {
                "loan_id": loan.generate_loan_id(),
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
        serializer.save(user=self.request.user)



# ✅ Loan Detail View
class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

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
                "loan_id": loan.generate_loan_id(),
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
