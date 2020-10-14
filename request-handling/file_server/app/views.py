import os
from datetime import datetime

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse


class FileInfo:
    def __init__(self, file: str):
        stat = os.stat(file)
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        self.name = os.path.basename(file)
        self.ctime = datetime.fromtimestamp(stat.st_ctime)
        self.mtime = datetime.fromtimestamp(stat.st_mtime)
        self.content = content


# Список полных путей к файлам в settings.FILES_PATH:
FILES = [os.path.join(settings.FILES_PATH, file) for file in os.listdir(settings.FILES_PATH)]


def file_list(request, date=None):
    template_name = 'index.html'

    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    files = [FileInfo(file) for file in FILES]
    if date:
        files = [file for file in files if file.ctime.date() == date]

    context = {
        'files': files,
        'date': date  # Этот параметр необязательный
    }

    return render(request, template_name, context)


def file_content(request, name: str):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    file = [f for f in FILES if name == os.path.basename(f)]
    if not file:
        return redirect(reverse(file_list))
    else:
        file_obj = FileInfo(file[0])

    return render(
        request,
        'file_content.html',
        context={'file_name': file_obj.name, 'file_content': file_obj.content}
    )
