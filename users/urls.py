from django.urls import path
from users import views

urlpatterns = [
    path('accounts/', views.ListCreateView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('accounts/newest/<int:num>/', views.ListUsersDateJoinedView.as_view())
]