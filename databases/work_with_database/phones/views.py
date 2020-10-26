from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from phones.models import Phone


def index(request):
    return redirect(reverse('catalog'))


def show_catalog(request):
    sort = request.GET.get('sort')
    sort_mapper = {'id': 'id', 'name': 'name', 'min_price': 'price', 'max_price': '-price'}

    if sort not in sort_mapper.keys():
        sort = 'id'

    phones = Phone.objects.order_by(sort_mapper[sort]).all()

    template = 'catalog.html'
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    slugs = [slug for (slug,) in Phone.objects.values_list('slug')]

    if slug not in slugs:
        return redirect(reverse('catalog'))
    else:
        phones = Phone.objects.filter(slug=slug)

    template = 'product.html'
    context = {'phones': phones}
    return render(request, template, context)
