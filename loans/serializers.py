from rest_framework import serializers
from .models import Loan
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from rest_framework import serializers

class LoanSerializer(serializers.ModelSerializer):
    monthly_installment = serializers.SerializerMethodField()
    total_interest = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    payment_schedule = serializers.SerializerMethodField()  # Ensure this is declared

    class Meta:
        model = Loan
        fields = [
            'id', 
            'user', 
            'amount', 
            'tenure', 
            'interest_rate', 
            'created_at', 
            'monthly_installment', 
            'total_interest', 
            'total_amount', 
            'payment_schedule'  # Include payment_schedule here
        ]
        read_only_fields = ['user', 'created_at']

    def get_monthly_installment(self, obj):
        return round(obj.calculate_monthly_installment(), 2)

    def get_total_interest(self, obj):
        return round(obj.calculate_total_interest(), 2)

    def get_total_amount(self, obj):
        return round(obj.calculate_total_payable(), 2)

    def get_payment_schedule(self, obj):
        return obj.generate_payment_schedule()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


# class LoanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Loan
#         fields = ['id', 'user', 'amount', 'tenure', 'interest_rate', 'created_at', 'is_foreclosed']