from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ListCreateView.as_view()),
    path('products/<pk>/', views.RetriveUpdateView.as_view())
]