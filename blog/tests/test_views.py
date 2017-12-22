from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User

from ..models import Post
from ..views import home

class HomeTests(TestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)