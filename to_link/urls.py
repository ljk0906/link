
from django.urls import include, path

from to_link.views import index, to_link, to

urlpatterns = [
    path(r'index/', index, name='index'),
    path(r'to_link/', to_link, name='to_link'),
    path(r'grade/', to)
]