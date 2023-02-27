from django.db import models

# Create your models here.

CATEGORIAS = (
    ('Programacao', 'Programação'),
    ('Design', 'Design'),
    ('Jogos_digitais', 'Jogos Digitais'),
    ('Mobile', 'Mobile'),
)

class Sala(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255)
    categoria = models.CharField(choices=CATEGORIAS, max_length=100)
    limite_participantes = models.IntegerField(default=50)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome