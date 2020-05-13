from django.db import models

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


  	def to_dict_json(self):
  		return{
  			'titulo': self.titulo,
  			'fonte': self.fonte,
  			'autores': self.autores,
  			'resumo': self.resumo,
  			'idioma': self.idioma,
  			'dataPrimeiroAcesso': self.dataPrimeiroAcesso,
        'categoria': self.categoria,
        'data_publicacao': self.data_publicacao,
        'jornal': self.jornal,
        'link_externo': self.link_externo
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

