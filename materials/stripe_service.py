import stripe

from config import settings


class StripeApi:

    stripe.api_key = settings.STRIPE_SECRET_KEY

    def __init__(self):
        self.stripe = stripe

    def get_products(self):
        return self.stripe.Product.list()

    def create_product(self, name, amount):
        product = self.stripe.Product.create(name=name)
        return self.stripe.Price.create(
            currency="usd",
            unit_amount=amount * 100,
            recurring={"interval": "month"},
            product=product.id,
        )

    def create_session(self, price_id):
        return self.stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
        )
