from django.test import SimpleTestCase
from django.urls import reverse, resolve
from salas_virtuais.views import *

class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_criar_sala_url_resolves(self):
        url = reverse('criar_sala')
        self.assertEquals(resolve(url).func, criar_sala)

    def test_editar_sala_url_resolves(self):
        url = reverse('editar_sala', args=[1])
        self.assertEquals(resolve(url).func, editar_sala)

    def test_excluir_sala_url_resolves(self):
        url = reverse('excluir_sala', args=[1])
        self.assertEquals(resolve(url).func, excluir_sala)