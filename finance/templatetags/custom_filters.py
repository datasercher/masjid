from django import template

register = template.Library()

@register.filter
def get_urdu_name(fund_type, fund_map):
    return fund_map.get(fund_type, fund_type)
