from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DeleteView

from .decorators import user_is_author_or_su, post_is_published, user_is_su
from .forms import NewPostForm
from .models import Post

# Create your views here.

def home(request):
    return render(request, 'home.html')
    
def about(request):
    return redirect('permanent_page', slug="about")
    
def contact(request):
    return redirect('permanent_page', slug="contact")
    
def permanent(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'permanent.html', {'post': post})

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog.html'
    queryset = Post.objects.order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        kwargs['link'] = 'view_post'
        return super().get_context_data(**kwargs)

@method_decorator(login_required, name='dispatch')
class AllPostListView(PostListView):
    def get_queryset(self):
        return super().get_queryset()

@method_decorator(user_is_su, name='dispatch')
class PermanentPostListView(PostListView):
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(category='P')
        return queryset
        
    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['link'] = 'permanent_page'
        return kwargs

class BlogPostListView(PostListView):
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(category='B').filter(published=True).filter(published_at__isnull=False)
        return queryset
        
    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['link'] = 'view_blog_post'
        return kwargs
    
@method_decorator(login_required, name='dispatch')
class BlogDraftListView(PostListView):
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(category='B').filter(Q(published_at__isnull=True) | Q(published=False))
        return queryset
        
    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['link'] = 'view_draft'
        return kwargs
            
class ArticlePostListView(PostListView):

    def get_queryset(self):
        queryset = super().get_queryset().filter(category='A').filter(published_at__isnull=False).filter(published=True)
        return queryset
        
    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['link'] = 'view_article_post'
        return kwargs

@method_decorator(login_required, name='dispatch')
class ArticleDraftListView(PostListView):
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(category='A').filter(Q(published_at__isnull=True) | Q(published=False))
        return queryset
        
    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['link'] = 'view_draft'
        return kwargs
        
class TagsListView(PostListView):
    def get_queryset(self):
        queryset = super().get_queryset().filter(tags__contains=self.kwargs['tag']).filter(published=True)
        return queryset
        
@login_required
def add_new_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(request.POST['title'])
            post.created_by = request.user
            
            published = request.POST.get('published', False)
            if published:
                post.published_at = timezone.now()
                url = 'post_list'
            else:
                url = 'draft_list'
                
            if post.category == "A":
                url = "article_" + url
            elif post.category == "B":
                url = "blog_" + url
            else:
                url = "home"
                
            try:
                post.save()
            except IntegrityError as e:
                return render(request, 'new_post.html', {'form': form, 'error': e})
            return redirect(url)
    else:
        form = NewPostForm()
    return render(request, 'new_post.html', {'form': form})

@post_is_published
def view_post(request, slug):
    #redirect to proper path in case a generic 'view_post' url is found
    post = get_object_or_404(Post, slug=slug)
    
    if request.resolver_match.url_name == 'view_post':
        if post.category is 'A':
            url = 'view_article_post'
        elif post.category is 'B':
            url = 'view_blog_post'
        else:
            url = 'home'
        return redirect(url, slug=slug)
    return render(request, 'post.html', {'post': post})

#@user_is_author_or_su
@login_required
def view_draft(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post.html', {'post': post})

@method_decorator(user_is_author_or_su, name='dispatch')
class EditPost(UpdateView):
    model = Post
    fields = ('title', 'snippet', 'message', 'tags', 'category', 'published')
    template_name = 'edit_post.html'
    #slug_url_kwarg = 'title'
    slug_field = 'slug'
    context_object_name = 'post'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        if post.published == True:
            if post.published_at is None:
                post.published_at = timezone.now()
            else:
                post.updated_at = timezone.now()
                post.updated_by = self.request.user
                
        post.save()
        
        if post.category is 'A':
            type = "article"
        else:
            type = "blog"
        
        if post.published is False or post.published_at is None:
            url = type + '_draft_list'
        else:
            url = type + '_post_list'
        
        return redirect(url)
        
@method_decorator(user_is_author_or_su, name='dispatch')
class DeletePost(DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    
    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs['slug'])
        if post.published == True:
            url = "post_list"
        else:  
            url = "draft_list"
            
        if post.category == "A":
            url = "article_" + url
        elif post.category == "B":
            url = "blog_" + url
        else:
            url = 'home'
        
        super().delete(self, request, *args, **kwargs)
        #sends a URL for JavaScript to handle redirection
        return HttpResponse(reverse_lazy(url))

def year(request, year):
    return HttpResponse("Hello World! It's " + str(year))
    
def month(request, year, month):
    return HttpResponse("Hello World! It's " + str(month) + "/" + str(year))
    
def day(request, year, month, date):
    return HttpResponse("Hello World! It's " + str(month) + "/" + str(date) + "/" + str(year))