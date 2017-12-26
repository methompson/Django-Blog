from datetime import date

from django import template
from django.urls import reverse
from django.utils.html import mark_safe

from ..models import Post

register = template.Library()

@register.filter
def menu_permanent_links(text):
    
    perm_links = Post.objects.filter(category='P').filter(published=True).order_by('slug')
    
    menu = ""
    
    for l in perm_links:
        menu += '<li class="nav-item active">'
        menu += '<a class="nav-link" href="{0}">{1}</a>'.format(reverse('permanent_page', kwargs={'slug':l.slug}), l.title)
        menu += '</li>'
        
    
    return mark_safe(menu)