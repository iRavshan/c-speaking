from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    path('practices/', views.practices, name='practices'),
    path('<str:answer_id>/', views.get_answer, name='answer'),
    path('logout/', views.Logout, name='logout'),
]