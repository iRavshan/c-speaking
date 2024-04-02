from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    path('practices/', views.practices, name='practices'),
    path('attempts/', views.attempts, name='attempts'),
    path('logout/', views.Logout, name='logout'),
    path('<str:answer_id>/', views.get_answer, name='answer'),
    path('attempts/<str:attempt_id>/', views.check_attempt, name='check_attempt'),
    path('attempts/<str:attempt_id>/', views.get_attempt, name='get_attempt'),
]