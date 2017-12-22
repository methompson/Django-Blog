from datetime import date

from django import template
from django.urls import reverse
from django.utils.html import mark_safe

register = template.Library()

@register.filter
def preview_text(text, link):
    end = text.find('</p>', 200)
    if end >= 200 :
        new_text = text[:end+4] + '<p><a href="' + link + '">Continue Reading</a></p>'
    else:
        new_text = text
    return mark_safe(new_text)
    
@register.filter
def style_tag(text, args):
    if args is None:
        return False
    arg_list = [arg.strip() for arg in args.split(',')]
    #search for a tag (arg_list[0]), then look for end of tag
    loc = 0
    while True:
        loc = text.find('<' + arg_list[0], loc)
        if loc >= 0:
            end = text.find('>', loc)
            tag = text[loc:end]
            #look for class
            #TODO add class name instead of skipping if class already exists.
            if 'class' not in tag:
                tag = tag.replace('<' + arg_list[0] , '<' + arg_list[0] + ' class=\"' + arg_list[1] + '\"')
                text = text[:loc] + tag + text[end:]
            loc = loc+1
        else:
            break
    #return text        
    return mark_safe(text)
    
@register.filter
def tag_links(text):
    tag_list = ""
    first = True
    for tag in text.split(','):
        
        if first:
            first = False
            pass
        else:
            tag_list = tag_list+', '
            
        tag_list = tag_list + '<a href="{0}">{1}</a>'.format(reverse('tag_list', kwargs={'tag': tag.strip()}), tag.strip())

    return mark_safe(tag_list)
        
@register.filter
def add_year(text):
    return date.today().year
        
    