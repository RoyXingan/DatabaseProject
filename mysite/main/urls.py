"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path(", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("curriculum", views.curriculum, name="curriculum"),
    path("course", views.course, name="course"),
    path("topic", views.topic, name="topic"),
    path("topic_set", views.topic_set, name="topic_set"),
    path("curriculum_course", views.curriculum_course, name="curriculum_course"),
    path("section", views.section, name="section"),
    path("goal", views.goal, name="goal"),
    path("grade_distribution", views.grade_distribution, name="grade_distribution"),
    path("query_one", views.query_one, name="query_one"),
    path("query_two", views.query_two, name="query_two"),
    path("query_three", views.query_three, name="query_three"),
]
