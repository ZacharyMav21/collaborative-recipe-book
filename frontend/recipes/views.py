from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests
from django.conf import settings
from django.shortcuts import render
from .forms import RecipeForm
from .models import Recipe, Ingredient
from django.shortcuts import redirect, get_object_or_404
def recipe_list(request):
    try:
        # Fetch recipes from the Flask API
        response = requests.get(f"{settings.FLASK_API_BASE_URL}/recipes")
        response.raise_for_status()
        recipes = response.json()
    except requests.exceptions.RequestException:
        recipes = []

    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})
def home(request):
    return render(request, 'home.html')
import requests
from django.shortcuts import render, redirect

def create_recipe(request):
    if request.method == 'POST':
        print(request.POST)  # Debug: Log the POST data

        title = request.POST.get('title')
        description = request.POST.get('description')
        instructions = request.POST.get('instructions')
        ingredients = request.POST.getlist('ingredients[]')  # Assuming array input

        payload = {
            'title': title,
            'description': description,
            'instructions': instructions,
            'ingredients': [{'name': i.split(':')[0], 'quantity': i.split(':')[1]} for i in ingredients]
        }

        response = requests.post('http://127.0.0.1:5000/recipes', json=payload)
        if response.status_code == 201:
            return redirect('recipe_list')  # Redirect to recipe list on success
        else:
            return render(request, 'recipes/create_recipe.html', {'error': response.json()})

    return render(request, 'recipes/create_recipe.html')

# Edit Recipe
def edit_recipe(request, id):
    # Fetch the recipe details from the Flask API
    try:
        response = requests.get(f"{settings.FLASK_API_BASE_URL}/recipes/{id}")
        response.raise_for_status()
        recipe_data = response.json()
    except requests.exceptions.RequestException as e:
        return render(request, 'recipes/error.html', {'error': str(e)})

    if request.method == 'POST':
        # Handle form submission
        title = request.POST.get('title')
        description = request.POST.get('description')
        instructions = request.POST.get('instructions')
        ingredients = request.POST.getlist('ingredients[]')

        payload = {
            'title': title,
            'description': description,
            'instructions': instructions,
            'ingredients': [{'name': i.split(':')[0], 'quantity': i.split(':')[1]} for i in ingredients],
        }

        try:
            put_response = requests.put(f"{settings.FLASK_API_BASE_URL}/recipes/{id}", json=payload)
            put_response.raise_for_status()
            return redirect('recipe_list')  # Redirect to the recipe list on success
        except requests.exceptions.RequestException as e:
            return render(request, 'recipes/edit_recipe.html', {'error': str(e), 'recipe': recipe_data})

    return render(request, 'recipes/edit_recipe.html', {'recipe': recipe_data})
# Recipe Details
def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

# Favorites Page
def favorites(request):
    favorite_recipes = Recipe.objects.filter(is_favorite=True)  # Assuming you have an `is_favorite` field
    return render(request, 'recipes/favorites.html', {'favorites': favorite_recipes})
def favorites_page(request):
    user_id = request.user.id  
    response = requests.get(f'http://127.0.0.1:5000/api/users/{user_id}/favorites')
    
    if response.status_code == 200:
        favorite_recipes = response.json()
    else:
        favorite_recipes = []

    return render(request, 'recipes/favorites.html', {'recipes': favorite_recipes})

def delete_recipe(request, id):
    try:
        # Send DELETE request to the Flask API
        response = requests.delete(f"{settings.FLASK_API_BASE_URL}/recipes/{id}")
        response.raise_for_status()  # Raise an error if the request failed
        return redirect('recipe_list')  # Redirect to the recipe list after successful deletion
    except requests.exceptions.RequestException as e:
        # Handle errors, such as network issues or API errors
        return render(request, 'recipes/error.html', {'error': str(e)})