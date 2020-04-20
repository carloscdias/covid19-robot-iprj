from django.urls import path, include
from app.views import WebPostList

urlpatterns = [
    path('', WebPostList.as_view(), name='post-list')
]