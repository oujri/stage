import time
import os
import uuid

from django.db import models
from django.utils.deconstruct import deconstructible

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


# For rename the file before save
@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        # eg: filename = 'my uploaded file.jpg'
        ext = filename.split('.')[-1]  # eg: 'jpg'
        uid = uuid.uuid4().hex[:10]  # eg: '567ae32f97'

        # eg: 'my-uploaded-file'
        new_name = '-'.join(filename.replace('.%s' % ext, '').split())

        # eg: 'my-uploaded-file_64c942aa64.jpg'
        renamed_filename = '%(new_name)s_%(uid)s.%(ext)s' % {'new_name': new_name, 'uid': uid, 'ext': ext}

        # eg: 'images/2017/01/29/my-uploaded-file_64c942aa64.jpg'
        return os.path.join(self.path, renamed_filename)


class Image(models.Model):
    description = models.CharField(max_length=255, blank=True)
    image_path = time.strftime('images/%Y/%m/%d')
    image = models.ImageField(upload_to=PathAndRename(image_path))
    datePublication = models.DateTimeField(auto_now_add=True)
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(262, 175)],
        format='JPEG',
        options={'quality': 100})
    image_video = ImageSpecField(
        source='image',
        processors=[ResizeToFill(600, 600)],
        format='JPEG',
        options={'quality': 100})

    def __str__(self):
        return self.image.name


class Publisher(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    tel = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    dateCreation = models.DateTimeField(auto_now_add=True, null=True)
    link = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    google = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    photoDeProfil = models.ForeignKey(Image, default=60, on_delete=models.SET(60))

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


class News(models.Model):
    titre = models.CharField(max_length=255)
    smallTitre = models.CharField(null=True, blank=True, max_length=255)
    contenu = models.TextField()
    datePublication = models.DateTimeField(auto_now_add=True)
    nombreVue = models.IntegerField(default=0)
    resume = models.TextField(blank=True, null=True)
    comment_enable = models.BooleanField(default=True, verbose_name='Activer les commentaires')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, blank=True, null=True, on_delete=models.CASCADE)
    imagePrincipale = models.ForeignKey(Image, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.titre

    def addVue(self):
        self.nombreVue += 1
        self.save()

    def sorted_comment(self):
        return self.commentaire_set.all().order_by('-nombreLike')

    class Meta:
        verbose_name_plural = 'News'


class Video(News):
    videoUrl = models.URLField()
    data_merge = models.IntegerField(default=2)
    equipe_selection = models.BooleanField(default=False)


class Comment(models.Model):
    nomComplet = models.CharField(max_length=50)
    datePublication = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    message = models.TextField()
    nombreLike = models.IntegerField(default=0)

    def like(self):
        self.nombreLike += 1
        self.save()

    def dislike(self):
        self.nombreLike -= 1
        self.save()

    def __str__(self):
        return self.nomComplet + ' ' + str(self.datePublication.date())

    class Meta:
        abstract = True


class Commentaire(Comment):
    news = models.ForeignKey(News, on_delete=models.CASCADE)


class Reponse(Comment):
    commentaire = models.ForeignKey(Commentaire, on_delete=models.CASCADE)


class Signal(models.Model):
    email = models.EmailField()
    motif = models.TextField()
    dateEnvoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email + '' + str(self.dateEnvoi.date())

    class Meta:
        abstract = True


class SignalComment(Signal):
    commentaire = models.ForeignKey(Commentaire, on_delete=models.CASCADE)


class SignalReponse(Signal):
    reponse = models.ForeignKey(Reponse, on_delete=models.CASCADE)


class Newsletter(models.Model):
    email = models.EmailField(primary_key=True)

    def __str__(self):
        return self.email


class CommentFilter(models.Model):
    word = models.CharField(max_length=50)

    def __str__(self):
        return self.word

    class Meta:
        verbose_name_plural = 'CommentsFilter'
