from django import template
register = template.Library()
from os import sys

from django.core.urlresolvers import resolve
import re
def is_active(context, url_name, class_name, default_class_name=""):
    
    if ('current_route_name' in context and (url_name == context['current_route_name'] or 
        re.search(url_name, context['current_route_name']))):
        return ' class="%s"' % (class_name,)
    elif default_class_name != "":
        return ' class="%s"' % (default_class_name,)
    else:
        return ''
register.simple_tag(takes_context=True)(is_active)


# Shortcode parser
from op_associazione.easycms import shortcode_parser

def shortcodes_replace(value):
        return shortcode_parser.parse(value)

register.filter('shortcodes', shortcodes_replace)

