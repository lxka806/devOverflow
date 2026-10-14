from django.urls import path
from . import views 

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login_user"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout, name="logout"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("<int:id>/", views.user_info, name="user_info"),
]

