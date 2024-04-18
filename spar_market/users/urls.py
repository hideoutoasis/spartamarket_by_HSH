from django.urls import path
from . import views

urlpatterns = [
    path("", views.users, name="users"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("<int:user_id>/follow/", views.follow, name="follow"),
]