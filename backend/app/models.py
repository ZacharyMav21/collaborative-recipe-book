from django.db import models
from . import db
from sqlalchemy.orm import relationship
recipe_ingredients = db.Table(
    'recipe_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id'), primary_key=True),
    db.Column('quantity', db.String(50))
)
# User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationships
    recipes = relationship("Recipe", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("Recipe", secondary="user_favorites", back_populates="favorited_by")

    def __repr__(self):
        return f"<User {self.username}>"

# Recipe model
class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_favorite = models.BooleanField(default=False)
    # Relationships
    author = relationship("User", back_populates="recipes")
    category = relationship("Category", back_populates="recipes")
    ingredients = relationship("Ingredient", secondary="recipe_ingredients", back_populates="recipes")
    comments = relationship("Comment", back_populates="recipe", cascade="all, delete-orphan")
    favorited_by = relationship("User", secondary="user_favorites", back_populates="favorites")

    def __repr__(self):
        return f"<Recipe {self.title}>"

# Ingredient model
class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationships
    recipes = relationship("Recipe", secondary="recipe_ingredients", back_populates="ingredients")

    def __repr__(self):
        return f"<Ingredient {self.name}>"

# Category model
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationships
    recipes = relationship("Recipe", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"

# Comment model
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationships
    recipe = relationship("Recipe", back_populates="comments")
    user = relationship("User", back_populates="comments")

    def __repr__(self):
        return f"<Comment {self.text[:20]}>"

# UserFavorites association table for many-to-many relationship between User and Recipe
class UserFavorites(db.Model):
    __tablename__ = 'user_favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
