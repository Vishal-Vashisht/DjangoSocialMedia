from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
# Create your models here.
User = get_user_model()
class profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField()
    profile_img = models.ImageField(upload_to='profile_img', default ='wink.png')
    location = models.CharField(max_length=100, blank=True)
    

    def _str_(self):
        return self.user.get_username


class Posts(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    post_image = models.ImageField(upload_to='Post_uploads')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class Postlike(models.Model):
    likepost_id = models.CharField(max_length=500)
    username = models.CharField(max_length=500)


    def __str__(self):
        return self.username

class Followers(models.Model):
    follower = models.CharField(max_length=500)
    user = models.CharField(max_length=200)

    def __str__(self):
        return self.user
    
    