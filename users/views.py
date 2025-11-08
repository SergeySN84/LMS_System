from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'course': ['exact'],
        'lesson': ['exact'],
        'payment_method': ['exact'],
    }
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user
