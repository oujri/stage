from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

from datetime import timedelta, datetime
from itertools import chain

from journal.models import Publisher
from .models import Categorie, Image, News, Video, Commentaire, Tag, Reponse, Newslatter
from .forms import ImageUploadForm, NewslatterForm, ReplyForm, SignalForm

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
    #one_week_ago = datetime.today() - timedelta(days=7)
    one_week_ago = datetime.today() - timedelta(days=21)
    #   T All
    tendance = News.objects.filter(datePublication__gte=one_week_ago).exclude(id__in=videoId).order_by('-nombreVue', '-id')[:10]
    #   T Style de vie
    categorie = Categorie.objects.get(name='styleDeVie')
    tstyledevie = News.objects.filter(categorie=categorie, datePublication__gte=one_week_ago).exclude(id__in=videoId).order_by('-nombreVue')[:8]
    #   T Sport
    categorie = Categorie.objects.get(name='sports')
    tsports = News.objects.filter(categorie=categorie, datePublication__gte=one_week_ago).exclude(id__in=videoId).order_by('-nombreVue')[:8]
    #   T Sport
    categorie = Categorie.objects.get(name='technologie')
    ttec = News.objects.filter(categorie=categorie, datePublication__gte=one_week_ago).exclude(id__in=videoId).order_by('-nombreVue')[:8]
    #   T Economie
    categorie = Categorie.objects.get(name='economie')
    teco = News.objects.filter(categorie=categorie, datePublication__gte=one_week_ago).exclude(id__in=videoId).order_by('-nombreVue')[:8]
    #   T Internationnal
    categorie = Categorie.objects.get(name='internationnal')
    tinter = News.objects.filter(categorie=categorie, datePublication__gte=one_week_ago).exclude(id__in=videoId).order_by('-nombreVue')[:8]

    # LAST ADD
    #   Internationnal
    categorie = Categorie.objects.get(name='internationnal')
    lastInter = News.objects.filter(categorie=categorie).exclude(id__in=videoId).order_by('-id')[:3]
    #   Economie
    categorie = Categorie.objects.get(name='economie')
    lastEco = News.objects.filter(categorie=categorie).exclude(id__in=videoId).order_by('-id')[:3]
    #   News
    categorie = Categorie.objects.get(name='actualites')
    lastNews = News.objects.filter(categorie=categorie).exclude(id__in=videoId).order_by('-id')[:5]

    # TOP_READ
    topRead = News.objects.all().exclude(id__in=videoId).order_by('-nombreVue', 'id')[:7]

    # TOP VIDEO
    topVideo = Video.objects.all().order_by('-nombreVue', '-id')[:5]

    # TOP COMMENTS
    topComment = Commentaire.objects.all().order_by('-nombreLike', '-datePublication')[:4]

    # LAST ADD
    #   LAST ADD NEWS
    lastAdd = News.objects.all().exclude(id__in=videoId).order_by('-datePublication')
    page = request.GET.get('page', 1)
    paginator = Paginator(lastAdd, 4)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    #   LAST ADD VIEDO
    lastAddVideo = Video.objects.all().order_by('-datePublication')[:4]
    #   LAST ADD COMMENT
    lastAddComment = Commentaire.objects.all().order_by('-datePublication')[:3]
    #   LAST ADD IMAGE
    lastAddImage = Image.objects.all().order_by('-datePublication')[:6]

    context = {
        'categories': Categorie.objects.all().exclude(name='actualites'),
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
        'lastAdd': articles,
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
    article.addVue()
    categorie = Categorie.objects.get(name=categorie)

    # ARTICLE TAGS
    tags = Tag.objects.filter(news=article)

    # ARTICLE COMMENT
    comments = Commentaire.objects.filter(news=article).order_by('-nombreLike')

    # MORE FROM AUTHOR
    moreArticle = News.objects.filter(publisher=article.publisher, categorie=article.categorie).exclude(id=article.id).order_by('-datePublication')[:4]
    if moreArticle.count() < 4:
        articleId = moreArticle.values_list('id', flat=True)
        number = 4 - moreArticle.count()
        addedArticle = News.objects.filter(publisher=article.publisher).exclude(id__in=articleId).order_by('-datePublication')[:number]
        moreArticle = list(chain(moreArticle, addedArticle))

    context = {
        'categories': Categorie.objects.all().exclude(name='actualites'),
        'weather': weather,
        'article': article,
        'categorie': categorie,
        'newslatterForm': NewslatterForm(),
        'signalForm': SignalForm(),
        'topRead': topRead,
        'topComment': topComment,
        'tags': tags,
        'replyForm': ReplyForm,
        'comments': comments,
        'moreArticle': moreArticle,
        'navActive': '#nav' + article.categorie.name
    }
    return render(request, 'journal/post.html', context)


def category(request, categorie):
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

    cat = Categorie.objects.get(name=categorie)

    filtre = request.GET.get('filtre', '-datePublication')

    news = News.objects.filter(categorie=cat).annotate(commentNumber=Count('commentaire'))

    # LAST FIVE
    lastFive = news.order_by(filtre, '-id')[:5]

    # OTHER ARTICLE
    lastFiveId = lastFive.values_list('id', flat=True)
    # other = news.exclude(id__in=lastFiveId).order_by(filtre)
    # for test
    other = News.objects.all().exclude(id__in=lastFiveId).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(other, 8)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        'categories': Categorie.objects.all().exclude(name='actualites'),
        'weather': weather,
        'topRead': topRead,
        'topComment': topComment,
        'newslatterForm': NewslatterForm(),
        'lastFive': lastFive,
        'category': cat,
        'articles': articles,
        'navActive': '#nav' + cat.name,
        'filtre': filtre
    }
    return render(request, 'journal/category.html', context)


def lastArticles(request):
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

    # FILTER
    filtre = request.GET.get('filtre', '-datePublication')
    news = News.objects.annotate(commentNumber=Count('commentaire'))

    # ARTICLES
    articles = news.order_by(filtre)
    page = request.GET.get('page', 1)
    paginator = Paginator(articles, 15)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        'categories': Categorie.objects.all().exclude(name='actualites'),
        'weather': weather,
        'topRead': topRead,
        'topComment': topComment,
        'newslatterForm': NewslatterForm(),
        'articles': articles,
        'filtre': filtre
    }
    return render(request, 'journal/lastArticles.html', context)


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


def comment(request, post):
    name = request.GET.get('name', None)
    email = request.GET.get('email', None)
    message = request.GET.get('message', None)
    if email is None:
        return redirect('index')
    c = News.objects.get(id=post).commentaire_set.create(nomComplet=name, email=email, message=message)
    data = {
        'message': 'Commentaire ajouté',
        'name': name,
        'comment': message,
        'date': c.datePublication
    }
    return JsonResponse(data)


def like(request, comment):
    type = request.GET.get('type', None)
    method = request.GET.get('method', None)
    c = Commentaire()
    if type == 'reponse':
        c = Reponse.objects.get(id=comment)
    elif type == 'comment':
        c = Commentaire.objects.get(id=comment)
    if method == 'like':
        c.like()
    elif method == 'dislike':
        c.dislike()
    data = {
        'nombre': str(c.nombreLike),
        'id': '#numberLike'+str(c.id),
        'div': '#divComment'+str(c.id)
    }
    return JsonResponse(data)


def signal(request, comment):
    type = request.GET.get('type', None)
    email = request.GET.get('email', None)
    motif = request.GET.get('motif', None)
    if type == 'reponse':
        Reponse.objects.get(id=comment).signalreponse_set.create(email=email, motif=motif)
    elif type == 'comment':
        Commentaire.objects.get(id=comment).signalcomment_set.create(email=email, motif=motif)
    data = {
        'message': 'Merci pour votre avertissement, nous allons consulter votre signal le plus tot possible',
        'formButton': '#formButtonSignaler'+str(comment),
        'formSignaler': '#signalForm'+str(comment),
        'paragraphe': '#messageSignal'+str(comment)
    }
    return JsonResponse(data)


def repondre(request, comment):
    email = request.GET.get('email', None)
    name = request.GET.get('name', None)
    message = request.GET.get('message', None)
    Commentaire.objects.get(id=comment).reponse_set.create(email=email, nomComplet=name, message=message)
    data = {
        'formRepondre': '#repondreForm' + str(comment),
        'formButtonRepondre': '#formButtonRepondre' + str(comment)
    }
    return JsonResponse(data)


def author(request, id):
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

    # AUTHOR
    aut = get_object_or_404(Publisher, id=id)

    # COMMENT NUMBER
    number = Commentaire.objects.filter(email=aut.email).count()

    # ARTICLES
    articles = aut.news_set.all().order_by('-datePublication')
    page = request.GET.get('page', 1)
    paginator = Paginator(articles, 14)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    # OTHER AUTHOR
    authors = Publisher.objects.annotate(newsCount=Count('news')).order_by('-newsCount')[:5]

    context = {
        'categories': Categorie.objects.all().exclude(name='actualites'),
        'weather': weather,
        'topRead': topRead,
        'topComment': topComment,
        'newslatterForm': NewslatterForm(),
        'author': aut,
        'articles': articles,
        'commentNumber': number,
        'authors': authors

    }
    return render(request, 'journal/author.html', context)
