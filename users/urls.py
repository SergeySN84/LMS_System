from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    PaymentViewSet,
    RegisterView,
    UserProfileView,
    SubscriptionToggleView,
    CreatePaymentView,
)

router = DefaultRouter()
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/profile/", UserProfileView.as_view(), name="profile"),
    path("api/subscribe/", SubscriptionToggleView.as_view(), name="subscribe"),
    path("api/payments/create/", CreatePaymentView.as_view(), name="create-payment"),
]
