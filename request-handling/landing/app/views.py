from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    landing_template = request.GET.get('from-landing')
    counter_click[landing_template] += 1
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    landing_template = request.GET.get('ab-test-arg')
    counter_show[landing_template] += 1
    if landing_template == 'original':
        return render(request, 'landing.html')
    elif landing_template == 'test':
        return render(request, 'landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    try:
        test_conversion = counter_click['test'] / counter_show['test']
    except ZeroDivisionError:
        test_conversion = 0

    try:
        original_conversion = counter_click['original'] / counter_show['original']
    except ZeroDivisionError:
        original_conversion = 0

    context = {'test_conversion': test_conversion,
               'original_conversion': original_conversion,
               }
    return render(request, 'stats.html', context=context)
