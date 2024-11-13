from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'category', 'instructions', 'is_favorite', 'ingredients']  # Add any fields from your model here
