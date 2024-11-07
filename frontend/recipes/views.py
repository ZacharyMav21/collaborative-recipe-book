from django.shortcuts import render
# recipes/views.py
import requests
from django.conf import settings
from django.shortcuts import render

def recipe_list(request):
    try:
        # Fetch recipes from the Flask API
        response = requests.get(f"{settings.FLASK_API_BASE_URL}/recipes")
        response.raise_for_status()
        recipes = response.json()
    except requests.exceptions.RequestException:
        recipes = []  # Handle any connection errors gracefully

    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})
def home(request):
    return render(request, 'home.html')