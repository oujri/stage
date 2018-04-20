from django.shortcuts import render, redirect

from .models import Categorie, Image, News
from .forms import ImageUploadForm

import requests


def index(request):

    # Meteo
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Rabat&units=metric&appid=91d3852842a30e80531df63b131af6d4'
    r = requests.get(url).json()
    weather = {
        'city': 'Rabat',
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    # Caroussel
    newsCar = News.objects.all().order_by('-id')[:3]

    # Tendance
    ## T Style de vie
    categorie = Categorie.objects.get(name='Style de vie')
    tstyledevie = News.objects.filter(categorie=categorie).order_by('-id')[:8]
    ## T Sport
    categorie = Categorie.objects.get(name='Sports')
    tsports = News.objects.filter(categorie=categorie).order_by('-id')[:8]
    ## T Sport
    categorie = Categorie.objects.get(name='Technologie')
    ttec = News.objects.filter(categorie=categorie).order_by('-id')[:8]

    context = {
        'categories': Categorie.objects.exclude(name='News').all(),
        'weather': weather,
        'newscar': newsCar,
        'tstyledevie': tstyledevie,
        'tsports': tsports,
        'ttec': ttec
    }
    return render(request, 'journal/index.html', context)


def about(request):
    return render(request, 'journal/about.html')


def contact(request):
    return render(request, 'journal/contact.html')


def privacy(request):
    return render(request, 'journal/privacy.html')


def post(request):
    # Meteo
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Rabat&units=metric&appid=91d3852842a30e80531df63b131af6d4'
    r = requests.get(url).json()
    weather = {
        'city': 'Rabat',
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    context = {
        'categories': Categorie.objects.exclude(name='News').all(),
        'weather': weather
    }
    return render(request, 'journal/post.html', context)


def upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            desc = request.POST['description']
            image = request.FILES['image']
            newImage = Image(description=desc, image=image)
            newImage.save()
            return redirect('upload')
    else:
        form = ImageUploadForm
    return render(request, 'temporary/imageUpload.html', {
        'form': form,
        'images': Image.objects.all()
    })
