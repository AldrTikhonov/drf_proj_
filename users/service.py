import os

import stripe
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv('API')


def create_product(product):
    """Создаем продукт для оплаты"""

    product_name = f"{product.course}" if product.course else f"{product.lesson}"
    product = stripe.Product.create(name=f"{product_name}")
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
        success_url="https://127.0.0.1:8000",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
