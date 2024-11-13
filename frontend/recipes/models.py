from django.db import models
from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField()
    category = models.CharField(max_length=100, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient')
    is_favorite = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.ingredient.name} - {self.quantity}'

class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)  # Replace with a real user model if you're using authentication
    
    def __str__(self):
        return f'{self.user} favorite - {self.recipe.title}'

