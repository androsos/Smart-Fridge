from django import template

register = template.Library()

@register.filter(name='subtract')
def subtract(value, arg):
    return int(value) - int(arg)

@register.filter(name='datediff')
def datediff(value, arg):
	delta = value - arg
	return int(delta.days)