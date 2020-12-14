from django import template
from crispy_forms.templatetags.crispy_forms_field import is_checkbox

register = template.Library()


@register.filter(name='add_classes')
def add_classes(value, arg):

    css_classes = value.field.widget.attrs.get('class', '')
    if css_classes:
        css_classes = css_classes.split(' ')
    else:
        css_classes = []

    args = arg.split(' ')
    for a in args:
        if a not in css_classes:
            css_classes.append(a)
    
    return value.as_widget(attrs={'class': ' '.join(css_classes)})


@register.filter(name='custom_field')
def custom_field(field):

    css_classes = field.css_classes()
    css_classes += 'bg-white border-left-0 border-md form-control'

    if field.errors:
        css_classes += ' is-invalid'
    
    return field.as_widget(attrs={'class': css_classes})


@register.filter
def provider_btn_class(provider):
    
    btn_class = ''
    if provider.name == 'Google':
        btn_class = 'btn-danger'
    if provider.name == 'Facebook':
        btn_class = 'btn-primary btn-facebook'
    if provider.name == 'GitHub':
        btn_class = 'btn-dark'
        
    return btn_class


@register.filter
def provider_color(provider):

    color = '#fff'
    if provider.name == 'Google':
        color = '#dc3545'
    if provider.name == 'Facebook':
        color = '#405d9d'
    if provider.name == 'GitHub':
        color = '#343a40'
        
    return color

@register.filter
def field_icon(field):

    icon = ''
    if field.name == 'email':
        icon = """<i class="far fa-envelope text-muted"></i>"""
    elif field.name == 'username':
        icon = """<i class="fas fa-user-friends text-muted"></i>"""
    elif field.name == 'password1' or field.name == 'password2':
        icon = """<i class="fas fa-key text-muted"></i>"""
    elif field.name == 'login':
        icon = """<i class="fa fa-user text-muted"></i>"""
    elif field.name == 'password':
        icon = """<i class="fas fa-key text-muted"></i>"""
    elif field.name == 'birth_date':
        icon = """<i class="fas fa-birthday-cake"></i>"""
    elif field.name == 'about':
        icon = """<i class="fas fa-address-card"></i>"""
    
    return icon
    
@register.filter
def di_r(field):

    print(dir(field), field.__dict__)
    
    return field