from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from materials.models import Course
from .models import Payment, User, Subscription
from .serializers import PaymentSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from .stripe_service import create_stripe_product, create_stripe_price, create_stripe_checkout_session


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

@extend_schema(
    summary="Переключить подписку на курс",
    description='Если подписка есть - удаляет, если нет - создает',
    request={"course_id": {"type": "integer"}},
    responses={200: {"message": {"type": "string"}}}
)


class SubscriptionToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({'error': 'course_id обязателен'}, status=400)

        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({'message': message})


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        if not course_id:
            return Response(
                {"error": "course_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)

        product = create_stripe_product(
            name=course.title,
            description=course.description or course.title
        )

        price = create_stripe_price(
            product_id=product["id"],
            amount=int(course.price * 100),  # $10.99 → 1099
            currency="usd"
        )

        success_url = "https://your-frontend.com/payment/success/"
        cancel_url = "https://your-frontend.com/payment/cancel/"

        session = create_stripe_checkout_session(
            price_id=price["id"],
            success_url=success_url,
            cancel_url=cancel_url
        )

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            payment_method="transfer",  # или "stripe"
            stripe_session_id=session["id"],
            stripe_payment_url=session["url"]
        )

        return Response({
            "payment_id": payment.id,
            "payment_url": session["url"]
        }, status=status.HTTP_201_CREATED)
