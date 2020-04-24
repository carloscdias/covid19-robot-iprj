from django.views.generic import ListView

from app.models import Novidade


class WebPostList(ListView):
    model = Novidade
    template_name = 'app/web_post_list.html'
