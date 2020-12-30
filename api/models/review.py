from django.db import models
from django.contrib.auth import get_user_model

class Review(models.Model):
  head = models.CharField(max_length=100)
  body = models.CharField(max_length=1000)
  rating = models.FloatField()
  game_id = models.ForeignKey('Game', related_name='reviews', on_delete=models.CASCADE)
  owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

  def __str__(self):
    return self.head

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'head': self.head,
        'body': self.body,
        'rating': self.rating
    }
