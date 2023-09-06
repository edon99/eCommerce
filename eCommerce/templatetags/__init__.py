from django.template import Library
from .quantityFilter import get_value
from .itemFilter import get_item

register = Library()

# Register the custom template filter
register.filter('get_value', get_value)
register.filter('get_item',get_item)