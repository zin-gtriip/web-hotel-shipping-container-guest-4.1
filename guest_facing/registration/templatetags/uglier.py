from django.template            import Library
from guest_facing.core          import utils

register = Library()

@register.filter()
def encrypt(value):
	return utils.encrypt(value)
