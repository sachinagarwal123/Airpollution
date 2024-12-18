"""
URL configuration for brainstack project.

The `urlpatterns` list routes URLs to views. For more information, see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from brainstackapp.views import insert_air_pollution_data,generate_air_pollution_diagram

urlpatterns = [
    path("admin/", admin.site.urls),
    path("insert-air-pollution-data/", insert_air_pollution_data, name="insert_air_pollution_data"),
    path("generate-air-pollution-diagram/", generate_air_pollution_diagram, name="generate_air_pollution_diagram"),
]
