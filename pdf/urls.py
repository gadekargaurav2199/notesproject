from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    
    path('', views.dashboard),
    path('upload/', views.upload),
    path('spark/', views.spark),
    path('profile/', views.profile),
    path('sign_up/', views.sign_up),
    path('view/<int:pk>/', views.view),
    path('delete/<int:pk>/', views.delete),
    path('view_profile/<int:pk>/', views.view_profile),
    path('logout/', views.logout),
    path('uploadpublication/', views.uploadpublication),
    path('test/', views.test),

]
