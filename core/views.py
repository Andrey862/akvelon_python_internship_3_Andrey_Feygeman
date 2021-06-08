from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from .models import Transaction
from .serializers import TransactionSerializer, GroupTransactionSerializer, FibonacciSerializer
from .permissions import IsTheOwnerOf
from .service import TransactionFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action


from rest_framework.negotiation import DefaultContentNegotiation
from django.db.models import Sum
from .utils import fibonacci

class TransactionViewSet(viewsets.ModelViewSet):
    """
    View set for ``Transaction``

    Function:
        ``list`` 
        ``retrive``
        ``update`` 
        ``partial_update``
        ``create`` 
        ``destoy``
        ``group_by_day``
    """
    queryset = Transaction.objects  
    serializer_class = TransactionSerializer
    permission_classes = [IsTheOwnerOf, IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False)
    def group_by_day(self, request: DefaultContentNegotiation):
        queryset = self.filter_queryset(self.get_queryset())
        aggregated = queryset.values('date').annotate(sum=Sum('amount')).order_by()

        serializer = GroupTransactionSerializer(aggregated, many=True)
        
        return Response(serializer.data)


class Fibonacci(GenericAPIView):
    serializer_class = FibonacciSerializer
    def post(self, request: DefaultContentNegotiation, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = fibonacci(serializer.data['n'])
        return Response({'result': result})
