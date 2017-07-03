""" Test sign up for stripe """
import logging
import os
from flask import Flask, request, redirect
import stripe

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

STRIPE_KEY = os.environ['STRIPE_KEY']

stripe.api_key = STRIPE_KEY

APP = Flask(__name__)

@APP.route("/", methods=["GET", "POST"])
def handler(event, context):
    """ Standard lambda handler """
    LOGGER.info('stripe key: %s', STRIPE_KEY)
    LOGGER.info('got event: %s', event)
    LOGGER.info('got context: %s', context)
    try:
        customer = stripe.Customer.create(
            email=request.form.get('stripeEmail'),
            source=request.form.get('stripeToken')
        )

        LOGGER.info('created customer: %s', customer)

        subscription = stripe.Subscription.create(
            customer=customer.id,
            plan="base-plan"
        )

        LOGGER.info('created subscription: %s', subscription)

        return redirect("https://clubjoe.co")

    except Exception as e:
        LOGGER.error('something went wrong')
        # Don't forget to log your errors before doing this!
        return redirect("https://www.google.com")

if __name__ == "__main__":
    APP.run()
