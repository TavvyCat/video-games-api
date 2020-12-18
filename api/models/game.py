from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Game(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  name = models.CharField(max_length=100, unique=True)
  description = models.CharField(max_length=10000)
  price = models.FloatField()

  def __str__(self):
    # This must return a string
    return self.name

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'name': self.name,
        'ripe': self.ripe,
        'color': self.color
    }
