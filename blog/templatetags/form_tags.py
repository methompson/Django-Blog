from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='get_widget')
def get_widget(field):
    type = field.field.widget.__class__.__name__
    return str(type)

@register.filter(name='set_class')
def set_class(field, arg):
    if field.form.is_bound:
        if field.errors:
            arg = arg + " is-invalid"
        else:
            arg = arg + " is-valid"
    return field.as_widget(attrs={'class': arg})
    
@register.filter(name='title')
@stringfilter
def title(value):
    return value.title()