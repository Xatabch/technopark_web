from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:id>/', views.question, name='question'),
    path('tag/<tagname>/', views.tag, name='tag'),
    path('hot/', views.hot, name='hot'),
    path('login/', views.signIn, name='signIn'),
    path('signup/', views.signUp, name='signUp'),
    path('ask/', views.ask, name='ask'),
    path('signOut/', views.signOut, name='signOut')
]

