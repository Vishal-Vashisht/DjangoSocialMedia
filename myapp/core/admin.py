from django.contrib import admin
from .models import profile, Posts, Postlike, Followers
# Register your models here.
social_models = [profile, Posts, Postlike, Followers]
admin.site.register(social_models)
