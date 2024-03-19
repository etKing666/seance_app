from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('start/', views.start, name='start'),
    path("about.html", views.about),
    path("contact.html", views.contact),
    path('index.html', views.index),
    path('start.html', views.start),
    path('layer1/', views.layer1, name='layer1'),
    path('complete.html', views.complete, name='complete')
]