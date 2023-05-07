from django.db import models

# Create your models here.

CATEGORIES = (
    ('Programacao', 'Programação'),
    ('Design', 'Design'),
    ('Jogos_digitais', 'Jogos Digitais'),
    ('Mobile', 'Mobile'),
)

class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORIES, max_length=100)
    max_participants = models.IntegerField(default=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name