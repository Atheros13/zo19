from django import template

register = template.Library()

@register.filter
def classname(obj):
    return obj.__class__.__name__

@register.filter
def objectfieldvalues(obj):
    obj_field_value = []
    for field in obj._meta.get_fields():
        f = field.name
        if f != 'id':
            try:
                obj_field_value.append((f, getattr(obj, f)))
            except:
                continue
    return obj_field_value