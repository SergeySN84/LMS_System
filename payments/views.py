from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from materials.models import Course
from users.models import Payment
from materials.stripe_service import create_stripe_product, create_stripe_price, create_stripe_session


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course_id')
        course = Course.objects.get(id=course_id)

        product = create_stripe_product(
            name=course.title,
            description=course.description or ""
        )

        price = create_stripe_price(
            product_id=product['id'],
            amount=int(course.price * 100),
            currency="usd"
        )

        success_url = "https://your-frontend.com/success"  # ← замените на ваш фронтенд
        cancel_url = "https://your-frontend.com/cancel"

        session = create_stripe_session(
            price_id=price['id'],
            success_url=success_url,
            cancel_url=cancel_url
        )

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            payment_method='transfer',  # или 'stripe'
            stripe_session_id=session['id'],
            stripe_payment_url=session['url']
        )

        return Response({
            "payment_id": payment.id,
            "payment_url": session['url']
        }, status=status.HTTP_201_CREATED)
