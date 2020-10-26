from django.shortcuts import render, redirect
from django.urls import reverse

from books.models import Book


def index(request):
    return redirect(reverse('books'))


def books_view(request, date=None):
    # Список всех книг. Выводим в context если дата не указана:
    books = Book.objects.all().order_by('-pub_date')
    context = {'books': books}
    if date:
        # Список всех дат:
        pub_dates = sorted({book.pub_date for book in books})
        # Переопределяем список books. Выбираем только книги с датой date:
        books = [book for book in books if book.pub_date == date]

        # Пишем собственный пагинатор с навигацией по датам:

        # Получаем индекс текущей даты в списке dates:
        current_page_index = pub_dates.index(date)

        # Через try/except получаем предыдущую и следующую даты если они есть:
        try:
            prev_page = pub_dates[current_page_index - 1]
        except IndexError:
            prev_page = None

        try:
            next_page = pub_dates[current_page_index + 1]
        except IndexError:
            next_page = None

        # Переопределям context полученными данными:
        context.update({'books': books, 'prev_page_url': prev_page, 'next_page_url': next_page})

    template = 'books/books_list.html'
    return render(request, template, context)
