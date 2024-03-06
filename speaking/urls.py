from django.urls import path
from . import views

urlpatterns = [
    path('mock/', views.Mock, name='mock'),
    path('part1/', views.Part1, name='speaking1'),
    path('part2/', views.Part2, name='speaking2'),
    path('part3/', views.Part3, name='speaking3'),
    path('save_answers/', views.save_answers, name='save_answers'),
]