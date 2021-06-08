from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from . import views


transactions = routers.SimpleRouter()
transactions.register('', views.TransactionViewSet)


urlpatterns = [
    path('transactions/', include(transactions.urls)),
    path('fibonacci/', views.Fibonacci.as_view()),
]