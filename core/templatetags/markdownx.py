# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify
from django.utils.safestring import SafeText

register = template.Library()


@register.filter()
def markdown(value, arg=None):
    print(type(value))
    markdown_raw = mark_safe(markdownify(value))
    if not isinstance(arg, dict) and arg is not None:
        arg = [arg]
        for i in arg:
            markdown_raw = markdown_raw.replace('</{}'.format(i[1:]), '')
            markdown_raw = markdown_raw.replace(i, '')
    return SafeText(markdown_raw)
