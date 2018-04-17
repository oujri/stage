from django.db import models


class Publisher(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    tel = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    link = models.URLField()
    facebook = models.URLField()
    twitter = models.URLField()
    youtube = models.URLField()
    instagram = models.URLField()

    def __str__(self):
        return self.nom + ' ' + self.prenom


class Categorie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class News(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    datePublication = models.DateTimeField(auto_now_add=True)
    categorie = models.ForeignKey(Categorie, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre
