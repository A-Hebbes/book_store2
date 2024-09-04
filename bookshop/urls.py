from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('bookshop/', views.my_shop, name='bookshop'),
    path('books/', views.books, name='books'),
]