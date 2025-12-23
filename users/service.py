import os

import stripe
from django.conf import settings

from courses.models import Course

stripe.api_key = settings.STRIPE_API_KEY


def create_product(payment):
    """Создаем продукт для оплаты"""
    course:Course = payment.course
    if course.stripe_id:
        return course.stripe_id

    product = stripe.Product.create(name=f"{course}")
    course.stripe_id = product.id
    course.save(update_fields=["stripe_id"])

    return product.id


def create_price(product, product_id):
    """Создаем цену для оплаты"""

    price = stripe.Price.create(
      currency="rub",
      unit_amount=product.amount * 100,
      product=product_id,
    )
    return price.get('id')


def create_session(price_id):
    """Создаем сессию для оплаты"""

    session = stripe.checkout.Session.create(
        success_url=settings.STRIPE_SUCCESS_URL,
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
