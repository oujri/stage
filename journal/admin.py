from django.contrib import admin

from .models import Publisher, Categorie, News, Image, Tag


admin.site.register(Publisher)
admin.site.register(Categorie)
admin.site.register(News)
admin.site.register(Image)
admin.site.register(Tag)
