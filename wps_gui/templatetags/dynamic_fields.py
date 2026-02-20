from django import template

register = template.Library()

@register.filter
def get_field_display(obj, field_name):
    # value = getattr(obj, field_name, '')
    value = obj.get(field_name, '')
    print(f"[DEBUG] {field_name} -> {value}") 
    return value