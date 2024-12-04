# frontend/recipes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.recipe_list, name='recipe_list'),
    path('create/', views.create_recipe, name='create_recipe'),
    path('edit/<int:id>/', views.edit_recipe, name='edit_recipe'),
    path('<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('favorites/', views.favorites, name='favorites'),
     path('delete/<int:id>/', views.delete_recipe, name='delete_recipe'),
]

