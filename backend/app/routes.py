from flask import Blueprint, request, jsonify
from .models import Recipe, Ingredient, recipe_ingredients
from . import db
from sqlalchemy import text
recipe_bp = Blueprint('recipes', __name__)

# Helper function to get ingredients with quantity
def get_ingredients_with_quantity(recipe_id):
    ingredients = []

    query = text("""
        SELECT ingredients.name, recipe_ingredients.quantity
        FROM ingredients
        JOIN recipe_ingredients ON ingredients.id = recipe_ingredients.ingredient_id
        WHERE recipe_ingredients.recipe_id = :recipe_id
    """)

    # Use .mappings() to get dictionary-like results
    result = db.session.execute(query, {'recipe_id': recipe_id}).mappings()

    for row in result:
        ingredients.append({
            'name': row['name'],
            'quantity': row['quantity']
        })

    return ingredients

# Route to get all recipes
@recipe_bp.route('/recipes', methods=['GET'])
def get_recipes():
    try:
        recipes = Recipe.query.all()
        recipe_list = [
            {
                'id': recipe.id,
                'title': recipe.title,
                'description': recipe.description,
                'instructions': recipe.instructions,
                'ingredients': get_ingredients_with_quantity(recipe.id)
            }
            for recipe in recipes
        ]
        return jsonify(recipe_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to create a new recipe
@recipe_bp.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    instructions = data.get('instructions')
    ingredients_data = data.get('ingredients', [])

    if not title or not description or not instructions:
        return jsonify({'error': 'Title, description, and instructions are required'}), 400

    try:
        # Step 1: Create the new recipe object
        new_recipe = Recipe(title=title, description=description, instructions=instructions)

        # Step 2: Add the recipe to the session
        db.session.add(new_recipe)
        db.session.commit()

        # Step 3: Insert into the recipe_ingredients association table
        for ing in ingredients_data:
            ingredient_name = ing.get('name')
            ingredient_quantity = ing.get('quantity')

            # Validate ingredient data
            if not ingredient_name or not ingredient_quantity:
                return jsonify({'error': 'Each ingredient must have a name and quantity'}), 400

            # Check if the ingredient exists, if not create a new one
            ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
            if not ingredient:
                ingredient = Ingredient(name=ingredient_name)
                db.session.add(ingredient)
                db.session.commit()

            # Insert into recipe_ingredients
            db.session.execute(
                recipe_ingredients.insert().values(
                    recipe_id=new_recipe.id,
                    ingredient_id=ingredient.id,
                    quantity=ingredient_quantity
                )
            )

        db.session.commit()
        return jsonify({'message': 'Recipe created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Route to get a single recipe
@recipe_bp.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    try:
        recipe_data = {
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'instructions': recipe.instructions,
            'ingredients': get_ingredients_with_quantity(recipe.id)
        }
        return jsonify(recipe_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to update a recipe
@recipe_bp.route('/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    data = request.get_json()
    recipe = Recipe.query.get(id)

    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    try:
        recipe.title = data.get('title', recipe.title)
        recipe.description = data.get('description', recipe.description)
        recipe.instructions = data.get('instructions', recipe.instructions)

        # Update ingredients if provided
        ingredients_data = data.get('ingredients', [])

        # Clear existing ingredients
        db.session.execute(
            recipe_ingredients.delete().where(recipe_ingredients.c.recipe_id == recipe.id)
        )

        # Add updated ingredients
        for ing in ingredients_data:
            ingredient_name = ing.get('name')
            ingredient_quantity = ing.get('quantity')

            if not ingredient_name or not ingredient_quantity:
                return jsonify({'error': 'Each ingredient must have a name and quantity'}), 400

            ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
            if not ingredient:
                ingredient = Ingredient(name=ingredient_name)
                db.session.add(ingredient)
                db.session.commit()

            db.session.execute(
                recipe_ingredients.insert().values(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id,
                    quantity=ingredient_quantity
                )
            )

        db.session.commit()
        return jsonify({'message': 'Recipe updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Route to delete a recipe
@recipe_bp.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get(id)

    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    try:
        db.session.delete(recipe)
        db.session.commit()
        return jsonify({'message': 'Recipe deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


