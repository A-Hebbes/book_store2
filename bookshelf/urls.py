from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bookshelf, name='view_bookshelf'),
    path('add/<book_id>/', views.add_to_bookshelf, name='add_to_bookshelf'),
]