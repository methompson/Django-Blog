from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe

from markdown import markdown
# Create your models here.

class CategoryField(models.Field):
    description = "Selection between multiple arbitrary values"
    #create list?
    
    def formfield(self, **kwargs):
        defaults = {'form_class': ChoiceField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

class Post(models.Model):
    CATEGORY_CHOICES = (
        ('A', 'Article'),
        ('B', 'Blog'),
        ('P', 'Permanent Page'),
    )
    
    title = models.CharField(max_length=1023)
    snippet = models.CharField(max_length=1023, blank=True, null=True) #Only used for previews
    message = models.TextField()
    published_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, null=True, related_name='posts', on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, blank=True, null=True, related_name='+', on_delete=models.SET_NULL)
    tags = models.CharField(blank=True, max_length=1023)
    tag_slugs = models.CharField(blank=True, max_length=1023)
    slug = models.SlugField(unique=True)
    published = models.BooleanField()
    
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES) #convert to choice between blog and article
    
    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message))
        
    def get_message_preview(self):
        text = markdown(self.message) #look for first closed paragraph
        par_end = str(text).find("</p>")
        
        #return everything up to end of paragraph. Paragraph closure is 4 characters long
        return mark_safe(text[:par_end+4])
        
    
    def __str__(self):
        return self.slug