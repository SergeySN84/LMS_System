from django.urls import path
from .views import CreatePaymentView

urlpatterns = [
    path('api/payments/create/', CreatePaymentView.as_view(), name='create-payment'),
]
