from django.views.generic import ListView
from django.shortcuts import render

from .models import Article


def articles_list(request):
    articles = Article.objects.select_related('genre').only('title', 'text', 'image', 'genre')
    template_name = 'articles/news.html'
    context = {'object_list': articles}

    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = '-published_at'

    return render(request, template_name, context)
