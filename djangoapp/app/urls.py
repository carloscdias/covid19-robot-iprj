from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

# from musics import views
from app.views import NovidadeViewSet, WebPostList

app_name = 'app'

router = DefaultRouter()
router.register(r'novidade/', NovidadeViewSet)

urlpatterns = [
    url(r'', WebPostList),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls))
]

