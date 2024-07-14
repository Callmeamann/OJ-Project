from django.db import models
from django.contrib.auth.models import User
from community.models import Community

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, default=3)
    followed_communities = models.ManyToManyField(Community, related_name='followers', blank=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
