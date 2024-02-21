from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    postContent = models.CharField(max_length = 140)
    postUser = models.ForeignKey(User, on_delete = models.CASCADE, related_name="author")
    postDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post: {self.id} by {self.postUser} on {self.postDate.strftime('%d/%m/%Y, %H:%M:%S')}"
    
class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")

    def __str__(self):
        return f"{self.following} is following {self.followed}"

class Like(models.Model):
    likingUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likingUser")
    likedPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likedPost")

    def __str__(self):
        return f"{self.likingUser} liked {self.likedPost}"