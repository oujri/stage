from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Publisher(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    tel = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

    def __str__(self):
        return self.nom + ' ' + self.prenom


class Categorie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=30, default='#37474F')
    icon = models.CharField(max_length=30, null=True, blank=True)
    tabHome = models.CharField(max_length=50, default='tab1')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    color = models.TextField(max_length=30, default='#37474F')

    def __str__(self):
        return self.name


class Image(models.Model):
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='uploads/images/')
    datePublication = models.DateTimeField(auto_now_add=True)
    lien = models.URLField(null=True, blank=True)
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(262, 175)],
        format='JPEG',
        options={'quality': 100})

    def __str__(self):
        return self.image.name


class News(models.Model):
    titre = models.CharField(max_length=255)
    smallTitre = models.CharField(default=titre, max_length=255)
    contenu = models.TextField()
    datePublication = models.DateTimeField(auto_now_add=True)
    nombreVue = models.IntegerField(default=0)
    resume = models.TextField(blank=True, null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, blank=True, null=True, on_delete=models.CASCADE)
    imagePrincipale = models.ForeignKey(Image, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name_plural = 'News'


class ImageVideo(Image):
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(600, 600)],
        format='JPEG',
        options={'quality': 100})


class Video(News):
    videoUrl = models.URLField()


class Commentaire(models.Model):
    nomComplet = models.CharField(max_length=50)
    datePublication = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    nombreLike = models.IntegerField(default=0)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomComplet + ' ' + self.datePublication


class Newslatter(models.Model):
    email = models.EmailField(primary_key=True)

    def __str__(self):
        return self.email
