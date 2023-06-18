from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

CATEGORIES = (
    ("Programacao", "Programação"),
    ("Design", "Design"),
    ("Jogos_digitais", "Jogos Digitais"),
    ("Mobile", "Mobile"),
)


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORIES, max_length=100)
    max_participants = models.IntegerField(default=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Roadmap(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    content = RichTextUploadingField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Document(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="media/", default="")
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
