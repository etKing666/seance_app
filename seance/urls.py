from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('contact/', views.contact),
    path("about.html", views.about),
    path("contact.html", views.contact),
    path('index.html', views.index)
]