from django.db import models
from django.contrib.auth import get_user_model

class Game(models.Model):
  title = models.CharField(max_length=100, unique=True)
  description = models.CharField(max_length=10000)
  price = models.FloatField()

  def __str__(self):
    return self.title

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'title': self.title,
        'description': self.description,
        'price': self.price
    }
