import stripe
import os
from django.conf import settings

stripe.api_key = os.getenv("STRIPE_KEY")

def create_product_course(course_title):
    create_payment = stripe.Product.create(name=course_title)
    return create_payment

def create_product_lesson(lesson_title):
    create_payment = stripe.Product.create(name=lesson_title)
    return create_payment

def create_price(product_id, amount):
    price = stripe.Price.create(unit_amount=int(amount * 100), currency='rub', product=product_id,)
    return price

def create_checkout_session(price_id):
    session = stripe.checkout.Session.create(payment_method_types=['card'], line_items=[{'price': price_id, 'quantity': 1}],
        mode='payment',
        success_url='http://localhost:8000/',
        cancel_url='http://localhost:8000/')
    return session