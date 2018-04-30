from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('upload/', views.upload, name='upload'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('comment/<int:post>/', views.comment, name='comment'),
    path('like/<int:comment>/', views.like, name='like'),
    path('signal/<int:comment>/', views.signal, name='signal'),
    path('repondre/<int:comment>/', views.repondre, name='repondre'),
    path('lastArticles/', views.lastArticles, name='lastArticles'),
    path('author/<int:id>/', views.author, name='author'),
    path('<slug:categorie>/<int:post>/', views.show, name='post'),
    path('<slug:categorie>/', views.category, name='category'),
]
