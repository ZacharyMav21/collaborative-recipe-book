# frontend/recipes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    # Add more paths as needed for the recipes app
]

