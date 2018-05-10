from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

from datetime import timedelta, datetime
from itertools import chain

from .models import Category, Image, News, Video, Comment, Tag, Answer, Newsletter, CommentFilter, Journalist
from .forms import ImageUploadForm, ReplyForm, SignalForm, JournalistProfileForm, JournalistImageUploadForm

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


#####################################################
#            PUBLIC PAGE REQUEST VIEW               #
#####################################################


# ## HOME PAGE ## #
def index(request):
    # VIDEO ID
    video_id = Video.objects.all().values_list('id', flat=True)

    # CAROUSEL
    new_car = News.objects.all().exclude(id__in=video_id).order_by('-id')[:3]

    # TRENDING : Get last week post ordering by view number and id
    # one_week_ago = datetime.today() - timedelta(days=7)
    one_week_ago = datetime.today() - timedelta(days=21)
    #   T All
    trending = News.objects.filter(date_publication__gte=one_week_ago).exclude(
        id__in=video_id).order_by('-view_number', '-id')[:10]
    #   T Style de vie
    t_category = Category.objects.get(name='styleDeVie')
    t_style_de_vie = News.objects.filter(category=t_category, date_publication__gte=one_week_ago).exclude(
        id__in=video_id).order_by('-view_number')[:8]
    #   T Sport
    t_category = Category.objects.get(name='sports')
    t_sports = News.objects.filter(category=t_category, date_publication__gte=one_week_ago).exclude(
        id__in=video_id).order_by('-view_number')[:8]
    #   T Sport
    t_category = Category.objects.get(name='technologie')
    t_tec = News.objects.filter(category=t_category, date_publication__gte=one_week_ago).exclude(
        id__in=video_id).order_by('-view_number')[:8]
    #   T ECONOMIE
    t_category = Category.objects.get(name='economie')
    t_eco = News.objects.filter(category=t_category, date_publication__gte=one_week_ago).exclude(
        id__in=video_id).order_by('-view_number')[:8]
    #   T Internationnal
    t_category = Category.objects.get(name='internationnal')
    t_inter = News.objects.filter(category=t_category, date_publication__gte=one_week_ago).exclude(
        id__in=video_id).order_by('-view_number')[:8]

    # LAST ADD
    #   Internationnal
    l_category = Category.objects.get(name='internationnal')
    last_inter = News.objects.filter(category=l_category).exclude(id__in=video_id).order_by('-id')[:3]
    #   Economie
    l_category = Category.objects.get(name='economie')
    last_eco = News.objects.filter(category=l_category).exclude(id__in=video_id).order_by('-id')[:3]
    #   News
    l_category = Category.objects.get(name='actualites')
    last_news = News.objects.filter(category=l_category).exclude(id__in=video_id).order_by('-id')[:5]

    # TOP VIDEO
    top_video = Video.objects.all().order_by('-view_number', '-id')[:5]

    # LAST ADD
    #   LAST ADD NEWS
    last_add = News.objects.all().exclude(id__in=video_id).order_by('-date_publication')
    page = request.GET.get('page', 1)
    paginator = Paginator(last_add, 4)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    #   LAST ADD VIDEO
    last_add_video = Video.objects.all().order_by('-date_publication')[:4]
    #   LAST ADD COMMENT
    last_add_comment = Comment.objects.all().order_by('-date_publication')[:3]
    #   LAST ADD IMAGE
    last_add_image = Image.objects.all().order_by('-date_publication')[:6]

    context = {
        'newscar': new_car,
        'tendance': trending,
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


# ## ABOUT PAGE ## #
def about(request):
    return render(request, 'journal/about.html')


# ## CONTACT PAGE ## #
def contact(request):
    return render(request, 'journal/contact.html')


# ## PRIVACY PAGE ## #
def privacy(request):
    return render(request, 'journal/privacy.html')


# ## IMAGE UPLOAD PAGE ## #
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


# ## SELECTED ARTICLE SHOW PAGE ## #
def article_show(request, category_name, post):
    # GET INFORMATION
    article = News.objects.get(id=post)
    article.add_view()

    # ARTICLE TAGS
    tags = Tag.objects.filter(news=article)

    # MORE FROM AUTHOR
    more_article = News.objects.filter(journalist=article.journalist, category=article.category).exclude(
        id=article.id).order_by('-date_publication')[:4]
    if more_article.count() < 4:
        article_id = more_article.values_list('id', flat=True)
        number = 4 - more_article.count()
        added_article = News.objects.filter(journalist=article.journalist).exclude(id__in=article_id)
        added_article = added_article.order_by('-date_publication')[:number]
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
        'signal_form': signal_form,
        'tags': tags,
        'reply_form': reply_form,
        'more_article': more_article,
        'navActive': '#nav' + article.category.name
    }
    return render(request, 'journal/post.html', context)


# ## ARTICLE CATEGORY PAGE ## #
def category(request, category_name):
    # VIDEO ID
    video_id = Video.objects.all().values_list('id', flat=True)

    cat = Category.objects.get(name=category_name)

    news_filter = request.GET.get('filter', '-date_publication')

    news = News.objects.filter(category=cat).annotate(comment_number=Count('comment')).exclude(id__in=video_id)

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
        'last_five': last_five,
        'category': cat,
        'articles': articles,
        'navActive': '#nav' + cat.name,
        'filter': news_filter
    }
    return render(request, 'journal/category.html', context)


# ## TAG PAGE ## #
def tag(request, tag_name):
    selected_tag = get_object_or_404(Tag, name=tag_name)

    # VIDEO ID
    video_id = Video.objects.all().values_list('id', flat=True)

    news_filter = request.GET.get('filter', '-date_publication')

    news = News.objects.filter(tag=selected_tag).annotate(comment_number=Count('comment')).exclude(id__in=video_id)

    count = news.count()

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
        'tag': selected_tag,
        'last_five': last_five,
        'articles': articles,
        'filter': news_filter,
        'count': count
    }

    return render(request, 'journal/tag.html', context)


# ## LAST ADDED ARTICLE PAGE ## #
def last_articles(request):
    # VIDEO ID
    video_id = Video.objects.all().values_list('id', flat=True)

    # FILTER
    news_filter = request.GET.get('filter', '-date_publication')
    news = News.objects.annotate(comment_number=Count('comment')).exclude(id__in=video_id)

    # ARTICLES
    articles = news.order_by(news_filter)
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
        'filter': news_filter
    }
    return render(request, 'journal/lastArticles.html', context)


# ## AUTHOR PAGE ## #
def author(request, selected_author_id):
    # AUTHOR
    aut = get_object_or_404(Journalist, id=selected_author_id)

    # COMMENT NUMBER
    number = Comment.objects.filter(email=aut.email).count()

    # ARTICLES
    articles = aut.news_set.all().order_by('-date_publication')

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
    authors = Journalist.objects.annotate(news_count=Count('news')).order_by('-news_count')[:5]

    context = {
        'author': aut,
        'articles': articles,
        'comment_number': number,
        'authors': authors

    }
    return render(request, 'journal/author.html', context)


# ## ALL VIDEO PAGE ## #
def video(request):
    # VIDEO SELECTION
    video_selection = Video.objects.filter(team_selection=True).order_by('-date_publication')[:5]

    # OTHER VIDEO
    other_video = Video.objects.all().order_by('-date_publication')
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


# ## SELECTED VIDEO SHOW PAGE ## #
def video_show(request, selected_video_id):
    # VIDEO
    selected_video = get_object_or_404(Video, id=selected_video_id)
    selected_video.add_view()

    # VIDEO TAGS
    tags = Tag.objects.filter(news=selected_video)

    # MORE FROM AUTHOR
    more_video = Video.objects.filter(journalist=selected_video.journalist, category=selected_video.category).exclude(
        id=selected_video.id).order_by('-date_publication')[:4]
    if more_video.count() < 4:
        video_id = more_video.values_list('id', flat=True)
        number = 4 - more_video.count()
        added_video = Video.objects.filter(journalist=selected_video.journalist).exclude(id__in=video_id).order_by(
            '-date_publication')[:number]
        more_video = list(chain(more_video, added_video))

    # LAST ADD VIDEO
    last_add_video = Video.objects.all().order_by('-date_publication')[:4]

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


# ## NEWS SEARCH PAGE ## #
def search(request):
    qs = News.objects.filter(active=True)
    keywords = request.GET.get('q')
    if keywords:
        query = SearchQuery(keywords)
        title_vector = SearchVector('title', weight='A')
        resume_vector = SearchVector('resume', weight='B')
        content_vector = SearchVector('content', weight='C')
        vectors = title_vector + content_vector + resume_vector
        qs = qs.annotate(search=vectors).filter(search=query)
        qs = qs.annotate(rank=SearchRank(vectors, query)).order_by('-rank', '-view_number')
    else:
        return redirect('index')

    count = qs.all().count()

    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 7)
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    context = {
        'article_result': qs,
        'search': keywords,
        'count': count
    }

    return render(request, 'journal/search.html', context)


#####################################################
#               AJAX REQUEST VIEW                   #
#####################################################


# ## NEWSLETTER SUBSCRIBE FUNCTION ## #
def subscribe(request):
    email = request.GET.get('email', None)
    if email is None:
        return redirect('index')
    data = {
        'is_taken': Newsletter.objects.filter(email=email).exists()
    }
    if data['is_taken']:
        data['message'] = 'Vous êtes déjà inscrit'
    else:
        registration = Newsletter(email=email)
        registration.save()
        data['message'] = 'Inscription effectué'
    return JsonResponse(data)


# ## COMMENT ARTICLE FUNCTION ## #
def comment(request, post):
    name = request.GET.get('name', None)
    email = request.GET.get('email', None)
    message = request.GET.get('message', None)
    if email is None:
        return redirect('index')

    comment_verify = True
    for c_filter in CommentFilter.objects.all():
        if c_filter.word in str(message):
            message = 'Commentaire inapproprié, veuillez vérifier les mots utilisés dans votre commentaire'
            comment_verify = False
            print(str(comment_verify))
            data = {
                'message': message,
                'accept': comment_verify
            }
            return JsonResponse(data)

    c = News.objects.get(id=post).comment_set.create(full_name=name, email=email, message=message)
    data = {
        'accept': comment_verify,
        'message': 'Commentaire ajouté',
        'name': name,
        'comment': message,
        'date': c.date_publication
    }
    return JsonResponse(data)


# ## LIKE AND DISLIKE COMMENT FUNCTION ## #
def like(request, selected_comment):
    comment_type = request.GET.get('type', None)
    method = request.GET.get('method', None)
    c = Comment()
    if comment_type == 'answer':
        c = Answer.objects.get(id=selected_comment)
    elif comment_type == 'comment':
        c = Comment.objects.get(id=selected_comment)
    if method == 'like':
        c.like()
    elif method == 'dislike':
        c.dislike()
    data = {
        'nombre': str(c.number_like),
        'id': '#numberLike'+str(c.id),
        'div': '#divComment'+str(c.id)
    }
    return JsonResponse(data)


# ## SIGNAL COMMENT AND REPLY FUNCTION ## #
def signal(request, selected_comment):
    comment_type = request.GET.get('type', None)
    email = request.GET.get('email', None)
    motif = request.GET.get('motif', None)
    if comment_type == 'answer':
        Answer.objects.get(id=selected_comment).signalanswer_set.create(email=email, cause=motif)
    elif comment_type == 'comment':
        Comment.objects.get(id=selected_comment).signalcomment_set.create(email=email, cause=motif)
    data = {
        'message': 'Merci pour votre avertissement, nous allons consulter votre signal le plus tot possible',
        'formButton': '#formButtonSignaler'+str(selected_comment),
        'formSignaler': '#signalForm'+str(selected_comment),
        'paragraphe': '#messageSignal'+str(selected_comment)
    }
    return JsonResponse(data)


# ## COMMENT REPLY FUNCTION ## #
def reply(request, selected_comment):
    email = request.GET.get('email', None)
    name = request.GET.get('name', None)
    message = request.GET.get('message', None)

    comment_verify = True
    for c_filter in CommentFilter.objects.all():
        if c_filter.word in str(message):
            message = 'Réponse inapproprié, veuillez vérifier les mots utilisés dans votre réponse'
            comment_verify = False
            print(str(comment_verify))
            data = {
                'message': message,
                'accept': comment_verify
            }
            return JsonResponse(data)

    Comment.objects.get(id=selected_comment).answer_set.create(email=email, full_name=name, message=message)
    data = {
        'accept': comment_verify,
        # 'formRepondre': '#repondreForm' + str(selected_comment), # For AJAX
        # 'formButtonRepondre': '#formButtonRepondre' + str(selected_comment) # For AJAX
    }
    return JsonResponse(data)


#####################################################
#            JOURNALIST MANAGEMENT VIEW             #
#####################################################

def journalist(request):
    if request.user.is_authenticated:
        user = request.user
        if user.email in Journalist.email_list():
            # VIDEO ID
            video_id = Video.objects.all().values_list('id', flat=True)

            # JOURNALIST
            j = get_object_or_404(Journalist, email=user.email)

            # STATISTIC
            # ## COMMENT COUNT
            number_comment = 0

            # ## NEWS COUNT
            # ## NEWS VIEW SUM
            number_news = 0
            news_views_sum = 0
            for n in News.objects.exclude(id__in=video_id).filter(journalist=j):
                number_news += 1
                news_views_sum += n.view_number
                number_comment += n.comment_set.count()

            # ## VIDEO COUNT
            # ## VIDEO VIEW SUM
            number_video = 0
            video_views_sum = 0
            for v in Video.objects.filter(journalist=j):
                number_video += 1
                video_views_sum += v.view_number
                number_comment += v.comment_set.count()

            # ## SELF COMMENT COUNT
            self_comment_count = Comment.objects.filter(email=j.email).count()

            statistic = {
                'number_comment': number_comment,
                'number_news': number_news,
                'news_views_sum': news_views_sum,
                'number_video': number_video,
                'video_views_sum': video_views_sum,
                'self_comment_count': self_comment_count
            }

            # TOP ARTICLE
            top_article = News.objects.exclude(id__in=video_id).filter(journalist=j).order_by('-view_number').first()

            # TOP VIDEO
            top_video = Video.objects.filter(journalist=j).order_by('-view_number').first()

            context = {
                'journalist': j,
                'statistic': statistic,
                'top_article': top_article,
                'top_video': top_video
            }
            return render(request, 'journal/journalist/journalist.html', context)

    return redirect('index')


def journalist_profile(request):

    if request.user.is_authenticated:
        user = request.user
        if user.email in Journalist.email_list():

            # JOURNALIST
            j = get_object_or_404(Journalist, email=user.email)

            form = JournalistProfileForm()
            message = 'null'
            message_image = 'null'

            if request.method == 'POST':

                if request.POST['method'] == 'image':
                    form_image = JournalistImageUploadForm(request.POST, request.FILES)
                    if form_image.is_valid():
                        img = Image(image=form_image.cleaned_data['image'], description='Profile image')
                        img.save()
                        j.profile_picture = img
                        j.save()
                        message_image = 'success'
                    else:
                        message_image = 'failed'

                else:
                    form = JournalistProfileForm(request.POST)

                    if form.is_valid():
                        cd = form.cleaned_data
                        user.username = cd['username']
                        user.save()

                        j.first_name = cd['first_name']
                        j.last_name = cd['last_name']
                        j.tel = cd['telephone']
                        j.link = cd['website']
                        j.facebook = cd['facebook']
                        j.twitter = cd['twitter']
                        j.instagram = cd['instagram']
                        j.youtube = cd['youtube']
                        j.google = cd['google_plus']
                        j.linkedin = cd['linkedin']
                        j.description = cd['description']
                        j.save()

                        message = 'Informations modifiées avec succès'

            # INFO
            number_comment = 0
            sum_views = 0
            for n in News.objects.filter(journalist=j):
                sum_views += n.view_number
                number_comment += n.comment_set.count()

            # FORM
            form.fields['username'].widget.attrs['value'] = user.username
            form.fields['telephone'].widget.attrs['value'] = j.tel
            form.fields['first_name'].widget.attrs['value'] = j.first_name
            form.fields['last_name'].widget.attrs['value'] = j.last_name
            form.fields['website'].widget.attrs['value'] = j.link
            form.fields['facebook'].widget.attrs['value'] = j.facebook
            form.fields['twitter'].widget.attrs['value'] = j.twitter
            form.fields['instagram'].widget.attrs['value'] = j.instagram
            form.fields['youtube'].widget.attrs['value'] = j.youtube
            form.fields['google_plus'].widget.attrs['value'] = j.google
            form.fields['linkedin'].widget.attrs['value'] = j.linkedin

            context = {
                'journalist': j,
                'form': form,
                'sum_views': sum_views,
                'number_comment': number_comment,
                'message': message,
                'form_image': JournalistImageUploadForm,
                'message_image': message_image
            }
            return render(request, 'journal/journalist/journalist-profile.html', context)

    return redirect('index')
