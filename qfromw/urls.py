from django.conf.urls import url
from . import views

urlpatterns = [
  # url(r'^$', views.appmain, name='appmain'),
  url(r'^$', views.input_word, name='input_word'),
]
