from journal.models import Categorie, Video, News, Commentaire
from journal.forms import NewslatterForm
import requests


def global_var(request):
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
    video_id = Video.objects.all().values_list('id', flat=True)
    top_read = News.objects.all().exclude(id__in=video_id).order_by('-nombreVue', 'id')[:7]

    # TOP COMMENTS
    top_comment = Commentaire.objects.all().order_by('-nombreLike', '-datePublication')[:4]

    context = {
        'categories': Categorie.objects.all().exclude(name='actualites'),
        'weather': weather,
        'topRead': top_read,
        'topComment': top_comment,
        'newslatterForm': NewslatterForm()
    }

    return context
