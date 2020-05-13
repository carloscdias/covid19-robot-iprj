from django.shortcuts import render
from django.http import JsonResponse
from app.models import Novidade


def WebPostList(request):
	return render(request, 'app/web_post_list.html')

def novidade_json(request):
	novidades = Novidade.objects.all()
	data = [novidade.to_dict_json() for novidade in novidades]
	response = {'data': data}
	return JsonResponse(response)
