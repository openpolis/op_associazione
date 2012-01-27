from django import template
register = template.Library()


from django.core.urlresolvers import resolve
import re
def is_active(context, url_name, class_name):
	if (url_name == context['current_route_name']) :
		return ' class="' + class_name +'"'
	if re.search(url_name, context['current_route_name']):
		return ' class="' + class_name +'"'
	return ''
register.simple_tag(takes_context=True)(is_active)


# Shortcode parser
from op_associazione.easycms import shortcode_parser

def shortcodes_replace(value):
        return shortcode_parser.parse(value)

register.filter('shortcodes', shortcodes_replace)

