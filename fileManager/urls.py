from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('feed/<str:pk>/', views.feed, name="feed"),
    path('create-feed/', views.createFeed, name='create-feed'),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('edit-feed/<str:pk>/', views.editFeed, name='edit-feed'),
    path('delete-feed/<str:pk>/', views.deleteFeed, name='delete-feed'),
    path('edit-comment/<str:pk>/', views.editComment, name='edit-comment'),
    path('delete-comment/<str:pk>/', views.deleteComment, name='delete-comment'),
    path('edit-user/', views.editUser, name="edit-user"),
    path('topics/', views.topicsPage, name="topics"),
]
