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
    #dump out on simple types
    if not hasattr(o, '_meta'):
        if isinstance(o, str): return mark_safe("'{0}'".format(o))
        if isinstance(o, int): return mark_safe("{0}".format(o))
        return mark_safe(json.dumps(o))

    so = serializers.serialize(
        'json',
        [o],
        indent=4
    )

    so_array = json.JSONDecoder().decode(so)
    so = so_array[0]

    #support either the core serializer (does pk) or
    #rest serializer (which prefers id)
    so['id'] = so['pk']
    jso = json.dumps(so)
    return mark_safe(jso)

@register.filter
def format_constants(c):
    properties = dir(c)
    output = dict()
    for property in properties:
        if property.isupper():
            output[property] = getattr(c, property)

    return mark_safe(json.dumps(output))

@register.filter
def forwardsort(o):
    return sorted(o)

@register.filter
def reversesort(o):
    return list(o.reverse())

