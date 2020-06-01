
from django.conf import settings
from rest_framework import serializers

from app.models import Novidade


class NovidadeSerializer(serializers.ModelSerializer):
    # If your <field_name> is declared on your serializer with the parameter required=False
    # then this validation step will not take place if the field is not included.
    data_publicacao = serializers.DateField(format=settings.DATE_FORMAT, required=False)
    dataPrimeiroAcesso = serializers.DateField(format=settings.DATE_FORMAT, required=False)
    class Meta:
    	model = Novidade
    	# fields = '__all__'
    	fields = ('resumo', 'titulo', 'idioma', 'autores', 'categoria', 'jornal', 'dataPrimeiroAcesso', 'fonte', 'link_externo')