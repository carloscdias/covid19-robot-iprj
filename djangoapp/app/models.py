from django.db import models
from django.db.models import Q
from model_utils import Choices
import ipdb

ORDER_COLUMN_CHOICES = Choices(
    ('0', 'resumo'),
    ('1', 'titulo'),
    ('2', 'autores'),
    ('3', 'categoria'),
    ('4', 'jornal'),
    ('5', 'dataPrimeiroAcesso'),
    ('6', 'data_publicacao'),
    ('7', 'fonte'),
    ('8', 'link_externo')
)

class PortalBusca(models.Model):
	nome = models.TextField()
	dataInclusao = models.DateField(auto_now_add=True)
	descricao = models.TextField()
	link = models.URLField()

class Novidade(models.Model):

    dataPrimeiroAcesso = models.DateField(auto_now_add=True)
    idioma = models.TextField()
    resumo = models.TextField(blank=True)
    autores = models.TextField(blank=True)
    fonte = models.URLField()
    link_externo = models.URLField(blank=True)
    jornal = models.TextField(blank=True)
    titulo = models.TextField(unique=True)
    categoria = models.TextField(blank=True)
    data_publicacao = models.TextField(blank=True)
    portalBusca = models.ForeignKey("PortalBusca", on_delete=models.CASCADE, null=True)
    credibilidade = models.ForeignKey("Credibilidade", on_delete=models.CASCADE, null=True)
    especialista = models.ForeignKey("Especialista", on_delete=models.CASCADE, null=True)

    class Meta:
      db_table = "app_novidade"

def query_posts_by_args(**kwargs):
  draw = int(kwargs.get('draw', None)[0])
  length = int(kwargs.get('length', None)[0])
  start = int(kwargs.get('start', None)[0])
  search_value = kwargs.get('search[value]', None)[0]
  order_column = kwargs.get('order[0][column]', None)[0]
  order = kwargs.get('order[0][dir]', None)[0]

  order_column = ORDER_COLUMN_CHOICES[order_column]
  # django orm '-' -> desc
  if order == 'desc':
    order_column = '-' + order_column

  queryset = Novidade.objects.all()
  total = queryset.count()

  if search_value:
    queryset = queryset.filter(Q(resumo__icontains=search_value) |
                                        Q(titulo__icontains=search_value) |
                                        Q(idioma__icontains=search_value) |
                                        Q(autores__icontains=search_value) |
                                        Q(categoria__icontains=search_value) |
                                        Q(jornal__icontains=search_value) |
                                        Q(dataPrimeiroAcesso__icontains=search_value) |
                                        Q(data_publicacao__icontains=search_value) |
                                        Q(fonte__icontains=search_value) |
                                        Q(link_externo__icontains=search_value) ) 


  count = queryset.count()
  queryset = queryset.order_by(order_column)[start:start + length]

  return{
  			'items': queryset,
  			'count': count,
  			'total': total,
  			'draw': draw
  		}

class Especialista(models.Model):
	nome = models.TextField()
	especialidade = models.TextField()

class Assunto(models.Model):
	descricao = models.TextField()
	palavrasChaves = models.TextField()
	dataInclusao = models.DateField()
	stringBusca = models.TextField()
	novidade = models.ManyToManyField("Novidade")

class AvisoPorEmail(models.Model):
	dataInicialRecebim = models.DateField()
	dataFinalRecebim = models.DateField()
	poisNovidade = models.TextField()
	credibilidadeAviso = models.ForeignKey("Credibilidade", on_delete=models.CASCADE)
	assuntoAviso = models.ForeignKey("Assunto", on_delete=models.CASCADE)
	pesquisador = models.ForeignKey("Pesquisador", on_delete=models.CASCADE)

class Credibilidade(models.Model):
	descricao = models.TextField()

class Pesquisador(models.Model):
	nome = models.TextField()

