from django.views.generic import ListView
from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    articles = Article.objects.prefetch_related().order_by('-published_at').all()
    context = {'object_list': articles}

    return render(request, template, context)
