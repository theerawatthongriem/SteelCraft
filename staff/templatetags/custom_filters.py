from django import template
from datetime import date

register = template.Library()

@register.filter
def days_until(ship_date):
    today = date.today()
    delta = ship_date - today
    return delta.days
