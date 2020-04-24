from django.db import models

class PortalBusca(models.Model):
	nome = models.TextField()
	dataInclusao = models.DateField(auto_now_add=True)
	descricao = models.TextField()
	link = models.URLField()

class Novidade(models.Model):
  	dataPrimeiroAcesso = models.DateField(auto_now_add=True)
  	idioma = models.TextField(blank=True)
  	resumo = models.TextField()
  	autores = models.TextField()
  	fonte = models.URLField(unique=True)
  	titulo = models.TextField()
  	portalBusca = models.ForeignKey("PortalBusca", on_delete=models.CASCADE, null=True)
  	credibilidade = models.ForeignKey("Credibilidade", on_delete=models.CASCADE, null=True)
  	especialista = models.ForeignKey("Especialista", on_delete=models.CASCADE, null=True)

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
