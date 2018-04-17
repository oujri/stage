from django.shortcuts import render

from .models import Categorie


def index(request):
    context = {
        'categories': Categorie.objects.exclude(name='News').all()
    }
    return render(request, 'journal/index.html', context)


def about(request):
    return render(request, 'journal/about.html')


def contact(request):
    return render(request, 'journal/contact.html')


def privacy(request):
    return render(request, 'journal/privacy.html')
