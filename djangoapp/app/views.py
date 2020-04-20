from django.views.generic import ListView

from app.models import WebPost


class WebPostList(ListView):
    model = WebPost
    template_name = 'app/web_post_list.html'
