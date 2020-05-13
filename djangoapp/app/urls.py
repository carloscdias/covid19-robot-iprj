from django.urls import path
from app.views import WebPostList, novidade_json

app_name = 'app'
urlpatterns = [
    path('', WebPostList, name='WebPostList'),
    path('novidade/json/', novidade_json, name='novidade_json')
]
