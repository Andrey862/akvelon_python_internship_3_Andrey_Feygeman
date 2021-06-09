from django.db.models import Sum
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
#from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.negotiation import DefaultContentNegotiation
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Transaction
from .permissions import IsTheOwnerOf
from .serializers import (FibonacciSerializer, GroupTransactionSerializer,
                          TransactionSerializer)
from .service import TransactionFilter
from .utils import fibonacci

from django.urls import get_resolver, reverse


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
        """
            returns transactions grouped by date with cumulative transaction amount
        """
        queryset = self.filter_queryset(self.get_queryset())
        aggregated = queryset.values('date').annotate(sum=Sum('amount')).order_by()

        serializer = GroupTransactionSerializer(aggregated, many=True)
        
        return Response(serializer.data)


class Fibonacci(GenericAPIView):
    serializer_class = FibonacciSerializer
    def put(self, request: DefaultContentNegotiation, *args, **kwargs):
        """
            returns Nth fibonacci number
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = fibonacci(serializer.data['n'])
        return Response({'result': result})
