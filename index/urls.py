"""ScoutingWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('events', EventViewSet, basename='event')
router.register('match', MatchViewSet, basename='match')
router.register('team', TeamViewSet, basename='team')

urlpatterns = [
    path('', MainPage),
    path('data/<str:event>/', EventPage),
    path('data/<str:event>/<int:level>/<int:num>/', MatchPage),
    path('data/<str:event>/<int:level>/<int:num>/<int:robot>/', RecordPage),
    path('data/<str:event>/<int:level>/<int:num>/<str:side>/', ScoutPage),
    path('data/<str:event>/team/<int:num>/', TeamPage),
    path('api/', include(router.urls)),
]
