from django.urls import path

from . import views

urlpatterns = [
    # VISITOR URL
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('upload/', views.upload, name='upload'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('comment/<int:post>/', views.comment, name='comment'),
    path('like/<int:selected_comment>/', views.like, name='like'),
    path('signal/<int:selected_comment>/', views.signal, name='signal'),
    path('reply/<int:selected_comment>/', views.reply, name='repondre'),
    path('lastArticles/', views.last_articles, name='lastArticles'),
    path('author/<int:selected_author_id>/', views.author, name='author'),
    path('video/', views.video, name='video'),
    path('video/<int:selected_video_id>/', views.video_show, name='video_show'),
    path('search/', views.search, name='search'),
    path('tag/<slug:tag_name>/', views.tag, name='tag'),

    # JOURNALIST URL
    path('journalist/', views.journalist, name='journalist'),
    path('journalist/journalist-profile/', views.journalist_profile, name='journalist_profile'),
    path('journalist/journalist_articles/', views.journalist_articles, name='journalist_articles'),
    path('journalist/create_article/', views.journalist_create_article, name='journalist_create_article'),
    path('journalist/update_article/<int:article_id>/', views.journalist_update_article,
         name='journalist_update_article'),
    path('journalist/cancel_article/', views.journalist_cancel_article, name="journalist_cancel_article"),

    # JOURNALIST AJAX URL
    path('journalist/upload_primary_image/', views.journalist_upload_primary_image,
         name='journalist_upload_primary_image'),
    path('journalist/update_primary_image/<int:article_id>/', views.journalist_update_primary_image,
         name='journalist_update_primary_image'),
    path('journalist/upload_image/', views.journalist_upload_image, name='journalist_upload_image'),
    path('journalist/update_image/<int:article_id>/', views.journalist_update_image, name='journalist_update_image'),
    path('journalist/create_tag/', views.journalist_create_tag, name='journalist_create_tag'),
    path('journalist/delete_image/<int:image_id>/', views.journalist_delete_image, name="journalist_delete_image"),
    path('journalist/delete_image_update/<int:article_id>/<int:image_id>/', views.journalist_delete_image_update,
         name="journalist_delete_image_update"),

    # CATEGORY AND SHOW ARTICLE
    path('<slug:category_name>/<int:post>/', views.article_show, name='post'),
    path('<slug:category_name>/', views.category, name='category'),

]
