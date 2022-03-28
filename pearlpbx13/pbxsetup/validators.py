from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_ipv4_address

import logging

logger = logging.getLogger(__name__)

''' Just example '''


def __validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )


def validate_bind_ip(value):
    items = value.split(':')
    logger.info(value)
    validate_ipv4_address(items[0])
    if len(items) > 1:
        try:
            port = int(items[1])
            if port < 1024 or port > 65535:
                raise ValidationError(
                    _('%(value)s is not a valid port'),
                    params={'value': items[1]},
                )
        except ValueError:
            raise ValidationError(
                _('%(value)s is not a valid port'),
                params={'value': items[1]},
            )
