"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import register_converter, path

from blog import views as blog_views
from blog import converters

register_converter(converters.FourDigitYearConverter, 'yyyy')
register_converter(converters.TwoDigitMonthConverter, 'mm')
register_converter(converters.TwoDigitDayConverter, 'dd')

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('new/', blog_views.add_new_post, name='add_new_post'),
    path('edit/<slug:slug>', blog_views.EditPost.as_view(), name='edit_post'),
    path('delete/<slug:slug>', blog_views.DeletePost.as_view(), name='delete_post'),
    path('all_posts/', blog_views.AllPostListView.as_view(), name='all_posts'),
    path('post/<slug:slug>', blog_views.view_post, name='view_post'),
    path('draft/<slug:slug>', blog_views.view_draft, name='view_draft'),
    
    path('blog/', blog_views.BlogPostListView.as_view(), name='blog_post_list'),
    path('blog/drafts/', blog_views.BlogDraftListView.as_view(), name='blog_draft_list'),
    path('blog/posts/<slug:slug>/', blog_views.view_post, name='view_blog_post'),
    path('blog/<yyyy:year>/', blog_views.year, name='year'),
    path('blog/<yyyy:year>/<mm:month>/', blog_views.month),
    path('blog/<yyyy:year>/<mm:month>/<dd:date>/', blog_views.day),
    path('articles/', blog_views.ArticlePostListView.as_view(), name='article_post_list'),
    path('articles/drafts', blog_views.ArticleDraftListView.as_view(), name='article_draft_list'),
    path('articles/posts/<slug:slug>/', blog_views.view_post, name='view_article_post'),
    
    path('', blog_views.home, name='home'),
    path('about', blog_views.about, name='about'),
    path('contact', blog_views.contact, name='contact'),
    path('site/<slug:slug>/', blog_views.permanent, name='permanent_page'),
    path('tags/<slug:tag>/', blog_views.TagsListView.as_view(), name='tag_list'),
    path('site/', blog_views.PermanentPostListView.as_view(), name='permanent_list'),
    
]

