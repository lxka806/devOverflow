from django.urls import path
from . import views 

urlpatterns = [
    path('', views.all_posts, name="main_page"),
    path("add/", views.create_question, name="add_questions")
]
