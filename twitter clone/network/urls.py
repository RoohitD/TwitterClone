
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.newPost, name="newPost"),
    path("profilePage/<int:user_id>", views.profilePage, name="profilePage"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("editPost/<int:post_id>", views.editPost, name="editPost"),
    path("likePost/<int:post_id>", views.likePost, name="likePost"),
    path("unlikePost/<int:post_id>", views.unlikePost, name="unlikePost"),
]
