from django.db import models

class WebPost(models.Model):
    """
    Esta classe representa uma entidade WebPost

    :cvar str title: titulo do post
    """
    title = models.TextField()