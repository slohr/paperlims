from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core import serializers

import logging
import json

logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
def classname(obj):
    return obj.__class__.__name__

# settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")

@register.filter
def jsonify(o):
    try:
        so = serializers.serialize(
            'json',
            [o]
        )
        # keeps formatting but it's an array
        #return mark_safe(json.JSONDecoder().decode(json.dumps(so)))

        so_array = json.JSONDecoder().decode(so)
        jso = json.dumps(so_array[0])
        return mark_safe(jso)
    except Exception as e:
        message = {
            'status': 'error',
            'message': '{0}'.format(e)
        }
        return mark_safe(json.dumps(message))

@register.filter
def forwardsort(o):
    return sorted(o)

@register.filter
def reversesort(o):
    return list(o.reverse())

