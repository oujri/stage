from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('privacy', views.privacy, name='privacy'),
    path('upload', views.upload, name='upload'),
    path('post', views.post, name='post'),
    path('subscribe', views.subscribe, name='subscribe')
]
