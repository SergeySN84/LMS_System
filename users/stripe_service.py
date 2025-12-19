import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name: str, description: str = ""):
    """Создаёт продукт в Stripe"""
    return stripe.Product.create(name=name, description=description or "")


def create_stripe_price(product_id: str, amount: int, currency: str = "usd"):
    """
    Создаёт цену в Stripe.
    """
    return stripe.Price.create(
        product=product_id,
        unit_amount=amount,
        currency=currency,
        recurring=None,  # one-time payment
    )


def create_stripe_checkout_session(price_id: str, success_url: str, cancel_url: str):
    """Создаёт сессию оплаты в Stripe Checkout"""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session
