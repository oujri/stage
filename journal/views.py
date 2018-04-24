from datetime import timedelta, datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from journal.models import Newslatter
from .models import Categorie, Image, News, Video, Commentaire, Tag
from .forms import ImageUploadForm, NewslatterForm

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

    videoId = Video.objects.all().values_list('id', flat=True)

    # Caroussel
    newsCar = News.objects.all().exclude(id__in=videoId).order_by('-id')[:3]

    # Tendance : Get last week post ordering by vue nomber and id
    one_week_ago = datetime.today() - timedelta(days=7)
    #   T All
    tendance = News.objects.filter(datePublication__gte=one_week_ago).exclude(id__in=videoId).order_by('-nombreVue', '-id')[:10]
    #   T Style de vie
    categorie = Categorie.objects.get(name='styleDeVie')
    tstyledevie = News.objects.filter(categorie=categorie, datePublication__gte=one_week_ago).exclude(id__in=videoId).order_by('-id')[:8]
    #   T Sport
    categorie = Categorie.objects.get(name='sports')
    tsports = News.objects.filter(categorie=categorie, datePublication__gte=one_week_ago).exclude(id__in=videoId).order_by('-id')[:8]
    #   T Sport
    categorie = Categorie.objects.get(name='technologie')
    ttec = News.objects.filter(categorie=categorie, datePublication__gte=one_week_ago).exclude(id__in=videoId).order_by('-id')[:8]
    #   T Economie
    categorie = Categorie.objects.get(name='economie')
    teco = News.objects.filter(categorie=categorie, datePublication__gte=one_week_ago).exclude(id__in=videoId).order_by('-id')[:8]
    #   T Internationnal
    categorie = Categorie.objects.get(name='internationnal')
    tinter = News.objects.filter(categorie=categorie, datePublication__gte=one_week_ago).exclude(id__in=videoId).order_by('-id')[:8]

    # LAST ADD
    #   Internationnal
    categorie = Categorie.objects.get(name='internationnal')
    lastInter = News.objects.filter(categorie=categorie).exclude(id__in=videoId).order_by('-id')[:3]
    #   Economie
    categorie = Categorie.objects.get(name='economie')
    lastEco = News.objects.filter(categorie=categorie).exclude(id__in=videoId).order_by('-id')[:3]
    #   News
    categorie = Categorie.objects.get(name='news')
    lastNews = News.objects.filter(categorie=categorie).exclude(id__in=videoId).order_by('-id')[:5]

    # TOP_READ
    topRead = News.objects.all().exclude(id__in=videoId).order_by('-nombreVue', 'id')[:7]

    # TOP VIDEO
    topVideo = Video.objects.all().order_by('-nombreVue', '-id')[:5]

    # TOP COMMENTS
    topComment = Commentaire.objects.all().order_by('-nombreLike', '-datePublication')[:4]

    # LAST ADD
    #   LAST ADD NEWS
    lastAdd = News.objects.all().exclude(id__in=videoId).order_by('-datePublication')[:4]
    #   LAST ADD VIEDO
    lastAddVideo = Video.objects.all().order_by('-datePublication')[:4]
    #   LAST ADD COMMENT
    lastAddComment = Commentaire.objects.all().order_by('-datePublication')[:3]
    #   LAST ADD IMAGE
    lastAddImage = Image.objects.all().order_by('-datePublication')[:6]

    context = {
        'categories': Categorie.objects.exclude(name='news').all(),
        'weather': weather,
        'newscar': newsCar,
        'tendance': tendance,
        'tstyledevie': tstyledevie,
        'tsports': tsports,
        'ttec': ttec,
        'teco': teco,
        'tinter': tinter,
        'lastEco': lastEco,
        'lastInter': lastInter,
        'lastNews': lastNews,
        'newslatterForm': NewslatterForm(),
        'topRead': topRead,
        'topVideo': topVideo,
        'lastAdd': lastAdd,
        'lastAddVideo': lastAddVideo,
        'lastAddComment': lastAddComment,
        'lastAddImage': lastAddImage,
        'topComment': topComment
    }
    return render(request, 'journal/index.html', context)


def about(request):
    return render(request, 'journal/about.html')


def contact(request):
    return render(request, 'journal/contact.html')


def privacy(request):
    return render(request, 'journal/privacy.html')


def upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload')
    else:
        form = ImageUploadForm
    return render(request, 'temporary/imageUpload.html', {
        'form': form,
        'images': Image.objects.all()
    })


def subscribe(request):
    email = request.GET.get('email', None)
    if email is None:
        return redirect('index')
    data = {
        'is_taken': Newslatter.objects.filter(email=email).exists()
    }
    if data['is_taken']:
        data['message'] = 'Vous êtes déjà inscrit'
    else:
        registration = Newslatter(email=email)
        registration.save()
        data['message'] = 'Inscription effectué'
    return JsonResponse(data)


def show(request, categorie, post):
    # Meteo
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Rabat&units=metric&appid=91d3852842a30e80531df63b131af6d4'
    r = requests.get(url).json()
    weather = {
        'city': 'Rabat',
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    # TOP_READ
    videoId = Video.objects.all().values_list('id', flat=True)
    topRead = News.objects.all().exclude(id__in=videoId).order_by('-nombreVue', 'id')[:7]

    # TOP COMMENTS
    topComment = Commentaire.objects.all().order_by('-nombreLike', '-datePublication')[:4]

    # GET INFORMATION
    article = News.objects.get(id=post)
    categorie = Categorie.objects.get(name=categorie)

    # ARTICLE TAGS
    tags = Tag.objects.filter(news=article)

    context = {
        'categories': Categorie.objects.exclude(name='news').all(),
        'weather': weather,
        'article': article,
        'categorie': categorie,
        'newslatterForm': NewslatterForm(),
        'topRead': topRead,
        'topComment': topComment,
        'tags': tags
    }
    return render(request, 'journal/post.html', context)


def category(request, categorie):
    id = Categorie.objects.get(name=categorie)
    return HttpResponse(str(id))
