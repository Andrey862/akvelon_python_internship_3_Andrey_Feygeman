from django.db.models import fields
from rest_framework import serializers
from .models import Transaction
from django.contrib.auth.models import User

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'created_at', 'amount', 'date', 'type')

class GroupTransactionSerializer(serializers.Serializer):
    date = serializers.DateField()
    sum = serializers.DecimalField(max_digits = 11, decimal_places=2)


class FibonacciSerializer(serializers.Serializer):
    n = serializers.IntegerField()

    def validate_n(self, value):
        if (value < 0):
            raise serializers.ValidationError("n must be greater or equal to 0")
        return value