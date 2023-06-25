from django import template
import json

register = template.Library()

@register.filter
def json_to_dict(value):
    try:
        json_value = json.loads(value)
        if isinstance(json_value, dict):
            return json_value.items()
    except (ValueError, TypeError):
        pass
    return {}

