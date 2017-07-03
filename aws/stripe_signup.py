""" Test sign up for stripe """
import logging
import urllib2
import os
from flask import Flask
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
        # get the body
        body = event['body']
        LOGGER.info('body: %s', body)
        # split the body
        tokens = body.split('&')
        LOGGER.info('tokens: %s', tokens)
        # get the email
        email_tokens = tokens[2].split('=')
        LOGGER.info('emailTokens: %s', email_tokens)
        encoded_email = email_tokens[1]
        email = urllib2.unquote(encoded_email)
        LOGGER.info('email: %s', email)
        # get the source
        source_tokens = tokens[0].split('=')
        LOGGER.info('sourceTokens: %s', source_tokens)
        source = source_tokens[1]

        # create the customer
        customer = stripe.Customer.create(email=email, source=source)
        LOGGER.info('created customer: %s', customer)

        # create the subscription
        plan = "base-plan"
        LOGGER.info('plan: %s', plan)
        subscription = stripe.Subscription.create(
            customer=customer.id,
            plan=plan
        )

        LOGGER.info('created subscription: %s', subscription)

        return {"location" : "https://clubjoe.co/signup_success"}

    except Exception as ex:
        LOGGER.info('error: %s', ex)
        LOGGER.error('something went wrong')

    return {"location" : "https://clubjoe.co/signup_error"}

if __name__ == "__main__":
    APP.run()
