from django.test import TestCase, Client
from django.urls import reverse
from salas_virtuais.models import Sala
import json
import datetime

class TestViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.index_url = reverse('index')
        self.criar_sala_url = reverse('criar_sala')
        self.editar_sala_url = reverse('editar_sala', args=[1])
        self.excluir_sala_url = reverse('excluir_sala', args=[1])

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html', 'base.html')

    def test_criar_sala_GET(self):
        response = self.client.get(self.criar_sala_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'criar_sala.html', 'base.html')

    def test_criar_sala_POST(self):
        sala01 = Sala.objects.create(
            id=1,
            nome='Sala 01',
            descricao='Sala de Programação',
            categoria='Programacao',
            limite_participantes=10,
            data_criacao=datetime.datetime.now()
        )

        response = self.client.post(self.criar_sala_url, {
            'nome': 'Sala 01',
            'descricao': 'Sala de Programação',
            'categoria': 'Programacao',
            'limite_participantes': 10,
            'data_criacao': str(datetime.datetime.now())
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(sala01.nome, 'Sala 01')
