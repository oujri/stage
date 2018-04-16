from django.shortcuts import render


def index(request):
    return render(request, 'journal/index.html')


def about(request):
    return render(request, 'journal/about.html')


def contact(request):
    return render(request, 'journal/contact.html')


def privacy(request):
    return render(request, 'journal/privacy.html')
