import logging

from django import template
from django.template.defaultfilters import stringfilter
import re
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)
register = template.Library()


@register.filter
@stringfilter
def recut(value, arg):
    return re.sub(arg, "", value)


@register.filter
@stringfilter
def recut1(value, arg):
    return re.sub(arg, "", value, 1)


@register.filter
@stringfilter
def reverse(value):
    return value[::-1]


@register.filter
@stringfilter
def stringcase(value, arg):
    allowed_args = ["camelcase", "capitalcase", "constcase", "lowercase", "pascalcase", "pathcase", "sentencecase", "snakecase", "spinalcase", "titlecase", "trimcase", "uppercase", "alphanumcase"]
    if arg not in allowed_args:
        raise ValueError(f"Expected arg in {allowed_args}. Received {arg}")
    f = import_string(f"stringcase.{arg}")
    return f(value)