import django_filters.rest_framework as filters
from .models import Transaction



class TransactionFilter(filters.FilterSet):
    class Meta:
        model = Transaction
        fields = {
            'created_at': ['lt', 'gt', 'exact'],
            'type': ['exact'],
            'date': ['lt', 'gt', 'exact'],
            'amount': ['lt', 'gt', 'exact'],
        }