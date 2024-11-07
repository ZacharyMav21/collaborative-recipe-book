# frontend/urls.py
from django.contrib import admin
from django.urls import path, include
from recipes import views  # Import views from recipes app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),  # Recipes URLs
    path('', views.home, name='home'),  # Home page at root URL
]
