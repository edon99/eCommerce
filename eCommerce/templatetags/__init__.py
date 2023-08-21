from django.template import Library
from .quantityFilter import get_value

register = Library()

# Register the custom template filter
register.filter('get_value', get_value)