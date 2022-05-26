import secrets

from django.conf import settings
from graphql_relay.node.node import from_global_id

from api.quiz.models import QuestionnaireResponses


def get_object(object_name, relay_id, otherwise=None):
    try:
        return object_name.filter.with_ids(from_global_id(relay_id)[1]).first()
    except:  # noqa
        return otherwise


def filter_objects(object_name, relay_ids, otherwise=None):
    if not isinstance(relay_ids, list):
        relay_ids = [relay_ids]
    try:
        object_ids = [from_global_id(relay_id)[1] for relay_id in relay_ids]
        return object_name.filter.with_ids(object_ids)
    except:  # noqa
        return otherwise


def generate_pin():
    pin = secrets.token_hex(settings.SHARABLE_PIN_BYTES_LENGTH)
    if QuestionnaireResponses.filter.with_pin(pin):
        return generate_pin()
    return pin
