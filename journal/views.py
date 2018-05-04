from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

from datetime import timedelta, datetime
from itertools import chain

from journal.models import Publisher
from .models import Categorie, Image, News, Video, Commentaire, Tag, Reponse, Newslatter
from .forms import ImageUploadForm, ReplyForm, SignalForm


#####################################################
#               PAGE REQUEST VIEW                   #
#####################################################


def index(request):
    # VIDEO ID
    video_id = Video.objects.all().values_list('id', flat=True)

    # CAROUSEL
    new_car = News.objects.all().exclude(id__in=video_id).order_by('-id')[:3]

    # TRENDING : Get last week post ordering by view number and id
    # one_week_ago = datetime.today() - timedelta(days=7)
    one_week_ago = datetime.today() - timedelta(days=21)
    #   T All
    tendance = News.objects.filter(datePublication__gte=one_week_ago).exclude(id__in=video_id).order_by('-nombreVue', '-id')[:10]
    #   T Style de vie
    t_category = Categorie.objects.get(name='styleDeVie')
    t_style_de_vie = News.objects.filter(categorie=t_category, datePublication__gte=one_week_ago).exclude(id__in=video_id).order_by('-nombreVue')[:8]
    #   T Sport
    t_category = Categorie.objects.get(name='sports')
    t_sports = News.objects.filter(categorie=t_category, datePublication__gte=one_week_ago).exclude(id__in=video_id).order_by('-nombreVue')[:8]
    #   T Sport
    t_category = Categorie.objects.get(name='technologie')
    t_tec = News.objects.filter(categorie=t_category, datePublication__gte=one_week_ago).exclude(id__in=video_id).order_by('-nombreVue')[:8]
    #   T ECONOMIE
    t_category = Categorie.objects.get(name='economie')
    t_eco = News.objects.filter(categorie=t_category, datePublication__gte=one_week_ago).exclude(id__in=video_id).order_by('-nombreVue')[:8]
    #   T Internationnal
    t_category = Categorie.objects.get(name='internationnal')
    t_inter = News.objects.filter(categorie=t_category, datePublication__gte=one_week_ago).exclude(id__in=video_id).order_by('-nombreVue')[:8]

    # LAST ADD
    #   Internationnal
    l_category = Categorie.objects.get(name='internationnal')
    last_inter = News.objects.filter(categorie=l_category).exclude(id__in=video_id).order_by('-id')[:3]
    #   Economie
    l_category = Categorie.objects.get(name='economie')
    last_eco = News.objects.filter(categorie=l_category).exclude(id__in=video_id).order_by('-id')[:3]
    #   News
    l_category = Categorie.objects.get(name='actualites')
    last_news = News.objects.filter(categorie=l_category).exclude(id__in=video_id).order_by('-id')[:5]

    # TOP VIDEO
    top_video = Video.objects.all().order_by('-nombreVue', '-id')[:5]

    # LAST ADD
    #   LAST ADD NEWS
    last_add = News.objects.all().exclude(id__in=video_id).order_by('-datePublication')
    page = request.GET.get('page', 1)
    paginator = Paginator(last_add, 4)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    #   LAST ADD VIDEO
    last_add_video = Video.objects.all().order_by('-datePublication')[:4]
    #   LAST ADD COMMENT
    last_add_comment = Commentaire.objects.all().order_by('-datePublication')[:3]
    #   LAST ADD IMAGE
    last_add_image = Image.objects.all().order_by('-datePublication')[:6]

    context = {
        'newscar': new_car,
        'tendance': tendance,
        'tstyledevie': t_style_de_vie,
        'tsports': t_sports,
        'ttec': t_tec,
        'teco': t_eco,
        'tinter': t_inter,
        'lastEco': last_eco,
        'lastInter': last_inter,
        'lastNews': last_news,
        'topVideo': top_video,
        'lastAdd': articles,
        'lastAddVideo': last_add_video,
        'lastAddComment': last_add_comment,
        'lastAddImage': last_add_image,
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


def show(request, category_name, post):
    # GET INFORMATION
    article = News.objects.get(id=post)
    article.addVue()
    selected_category = Categorie.objects.get(name=category_name)

    # ARTICLE TAGS
    tags = Tag.objects.filter(news=article)

    # MORE FROM AUTHOR
    more_article = News.objects.filter(publisher=article.publisher, categorie=article.categorie).exclude(id=article.id).order_by('-datePublication')[:4]
    if more_article.count() < 4:
        article_id = more_article.values_list('id', flat=True)
        number = 4 - more_article.count()
        added_article = News.objects.filter(publisher=article.publisher).exclude(id__in=article_id).order_by('-datePublication')[:number]
        more_article = list(chain(more_article, added_article))

    # DYNAMIC COMMENT FORM
    reply_form = ReplyForm()
    signal_form = SignalForm()
    if request.user.is_authenticated:
        reply_form.fields['email'].widget.attrs['hidden'] = 'true'
        reply_form.fields['email'].widget.attrs['value'] = request.user.email
        reply_form.fields['name'].widget.attrs['hidden'] = 'true'
        reply_form.fields['name'].widget.attrs['value'] = request.user
        signal_form.fields['email'].widget.attrs['hidden'] = 'true'
        signal_form.fields['email'].widget.attrs['value'] = request.user.email

    context = {
        'article': article,
        'categorie': selected_category,
        'signalForm': signal_form,
        'tags': tags,
        'replyForm': reply_form,
        'moreArticle': more_article,
        'navActive': '#nav' + article.categorie.name
    }
    return render(request, 'journal/post.html', context)


def category(request, category_name):
    # VIDEO ID
    video_id = Video.objects.all().values_list('id', flat=True)

    cat = Categorie.objects.get(name=category_name)

    news_filter = request.GET.get('filtre', '-datePublication')

    news = News.objects.filter(categorie=cat).annotate(commentNumber=Count('commentaire')).exclude(id__in=video_id)

    # LAST FIVE
    last_five = news.order_by(news_filter, '-id')[:5]

    # OTHER ARTICLE
    last_five_id = last_five.values_list('id', flat=True)
    # other = news.exclude(id__in=lastFiveId).order_by(news_filter)
    # for test
    other = News.objects.all().exclude(id__in=last_five_id).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(other, 8)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        'lastFive': last_five,
        'category': cat,
        'articles': articles,
        'navActive': '#nav' + cat.name,
        'filtre': news_filter
    }
    return render(request, 'journal/category.html', context)


def last_articles(request):
    # VIDEO ID
    video_id = Video.objects.all().values_list('id', flat=True)

    # FILTER
    filtre = request.GET.get('filtre', '-datePublication')
    news = News.objects.annotate(commentNumber=Count('commentaire')).exclude(id__in=video_id)

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
        'articles': articles,
        'filtre': filtre
    }
    return render(request, 'journal/lastArticles.html', context)


def author(request, id):
    # AUTHOR
    aut = get_object_or_404(Publisher, id=id)

    # COMMENT NUMBER
    number = Commentaire.objects.filter(email=aut.email).count()

    # ARTICLES
    articles = aut.news_set.all().order_by('-datePublication')

    for a in articles:
        if isinstance(a, Video):
            print('Video')

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
        'author': aut,
        'articles': articles,
        'commentNumber': number,
        'authors': authors

    }
    return render(request, 'journal/author.html', context)


def video(request):
    # VIDEO SELECTION
    video_selection = Video.objects.filter(equipe_selection=True).order_by('-datePublication')[:5]

    # OTHER VIDEO
    other_video = Video.objects.all().order_by('-datePublication')
    page = request.GET.get('page', 1)
    paginator = Paginator(other_video, 10)
    try:
        other_video = paginator.page(page)
    except PageNotAnInteger:
        other_video = paginator.page(1)
    except EmptyPage:
        other_video = paginator.page(paginator.num_pages)

    context = {
        'video_selection': video_selection,
        'other_video': other_video
    }

    return render(request, 'journal/video.html', context)


def video_show(request, id):
    # VIDEO
    selected_video = get_object_or_404(Video, id=id)
    selected_video.addVue()

    # VIDEO TAGS
    tags = Tag.objects.filter(news=selected_video)

    # MORE FROM AUTHOR
    more_video = Video.objects.filter(publisher=selected_video.publisher, categorie=selected_video.categorie).exclude(
        id=selected_video.id).order_by('-datePublication')[:4]
    if more_video.count() < 4:
        video_id = more_video.values_list('id', flat=True)
        number = 4 - more_video.count()
        added_video = Video.objects.filter(publisher=selected_video.publisher).exclude(id__in=video_id).order_by(
            '-datePublication')[:number]
        more_video = list(chain(more_video, added_video))

    # LAST ADD VIDEO
    last_add_video = Video.objects.all().order_by('-datePublication')[:4]

    # DYNAMIC COMMENT FORM
    reply_form = ReplyForm()
    signal_form = SignalForm()
    if request.user.is_authenticated:
        reply_form.fields['email'].widget.attrs['hidden'] = 'true'
        reply_form.fields['email'].widget.attrs['value'] = request.user.email
        reply_form.fields['name'].widget.attrs['hidden'] = 'true'
        reply_form.fields['name'].widget.attrs['value'] = request.user
        signal_form.fields['email'].widget.attrs['hidden'] = 'true'
        signal_form.fields['email'].widget.attrs['value'] = request.user.email

    context = {
        'video': selected_video,
        'tags': tags,
        'more_video': more_video,
        'lastAddVideo': last_add_video,
        'signalForm': signal_form,
        'replyForm': reply_form,
    }

    return render(request, 'journal/video_view.html', context)


#####################################################
#               AJAX REQUEST VIEW                   #
#####################################################


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
    comment_type = request.GET.get('type', None)
    method = request.GET.get('method', None)
    c = Commentaire()
    if comment_type == 'reponse':
        c = Reponse.objects.get(id=comment)
    elif comment_type == 'comment':
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
    comment_type = request.GET.get('type', None)
    email = request.GET.get('email', None)
    motif = request.GET.get('motif', None)
    if comment_type == 'reponse':
        Reponse.objects.get(id=comment).signalreponse_set.create(email=email, motif=motif)
    elif comment_type == 'comment':
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
