from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=100)

class Post(models.Model):
    text = models.CharField(max_length=300)
    price = models.IntegerField(default=0)
    sold = models.BooleanField(default=False)
    date = models.DateTimeField('date published')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    def __str__(self):
        return self.text
