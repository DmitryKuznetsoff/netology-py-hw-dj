from django.http import HttpResponse
from django.shortcuts import render, reverse
import os
from django.utils import timezone


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время':  reverse('time'),
        'Показать содержимое рабочей директории':  reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    current_time = timezone.localtime().astimezone().time()
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей 
    # директории
    cwd_content = os.listdir(os.curdir)
    cwd_content = map(lambda x: x+'/' if os.path.isdir(x) else x, cwd_content)
    msg = f"Содержимое папки {os.path.basename(os.getcwd())}: </br>{'</br>'.join(cwd_content)}"

    return HttpResponse(msg)
