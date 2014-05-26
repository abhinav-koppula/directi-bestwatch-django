from django import template
register = template.Library()

def check_profpic(value):
    if value[-1] == 'e' and value[-2] == 'g' and value[-3] == 'r':
        return value
    else:
        return '/static/img/temp/profpics/'+value

@register .simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''

register.filter('check_profpic', check_profpic)
