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
def create_recipe(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        category = request.POST['category']
        instructions = request.POST['instructions']
        favorite = 'favorite' in request.POST

        # Create the Recipe instance
        recipe = Recipe.objects.create(
            title=title,
            description=description,
            category=category,
            instructions=instructions,
            favorite=favorite
        )

        # Handle ingredients
        ingredient_names = request.POST.getlist('ingredient_name[]')
        ingredient_quantities = request.POST.getlist('ingredient_quantity[]')

        for name, quantity in zip(ingredient_names, ingredient_quantities):
            Ingredient.objects.create(
                recipe=recipe,
                name=name,
                quantity=quantity
            )

        return redirect('recipe_list')  # Redirect to a list or detail page

    return render(request, 'recipes/create_recipe.html')
# Edit Recipe
def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.method == 'PATCH':
        form = RecipeForm(request.PATCH, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', id=id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/edit_recipe.html', {'form': form, 'recipe': recipe})

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