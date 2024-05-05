from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('start/', views.start, name='start'),
    path('apology/', views.apology, name='apology'),
    path('complete/', views.complete, name='complete'),
    path("about.html", views.about),
    path("contact.html", views.contact),
    path('index.html', views.index),
    path('start.html', views.start),
    path('questions/', views.questions, name='questions'),
    path('complete.html', views.complete),
    path('apology.html', views.apology)
]


