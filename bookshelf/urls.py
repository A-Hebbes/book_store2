from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bookshelf, name='view_bookshelf'),
    path('add/<book_id>/', views.add_to_bookshelf, name='add_to_bookshelf'),
    path('adjust/<int:book_id>/', views.adjust_bookshelf, name='adjust_bookshelf'),
    path('remove/<book_id>/', views.remove_from_bookshelf, name='remove_from_bookshelf'),
]