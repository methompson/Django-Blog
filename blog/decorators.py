from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from blog.models import Post

def user_is_author_or_su(function):
    def wrap(request, *args, **kwargs):
        post = Post.objects.get(slug=kwargs['slug'])
        if post.created_by == request.user or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return redirect('home')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
    
def user_is_su(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return redirect('home')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
    
def post_is_published(function):
    def wrap(request, *args, **kwargs):
        post = Post.objects.get(slug=kwargs['slug'])
        if post.published_at is None or post.published is False:
            return redirect('home')
        else:
            return function(request, *args, **kwargs)
        
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap