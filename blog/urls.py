from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("categorie/<slug:slug>/", views.posts_by_category, name="posts_by_category"),
    path("tag/<slug:slug>/", views.posts_by_tag, name="posts_by_tag"),
]
