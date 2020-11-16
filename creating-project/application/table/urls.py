from django.urls import path

from table.views import table_view

urlpatterns = [
    path('', table_view, name='table')
]
