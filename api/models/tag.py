from django.db import models
from django.contrib.auth import get_user_model

class Tag(models.Model):
  name = models.CharField(max_length=100)
  game_id = models.ForeignKey('Game', related_name='tags', on_delete=models.CASCADE)
  owner = models.ForeignKey('User', related_name='tags', on_delete=models.CASCADE)

  def __str__(self):
    return self.genre

  def as_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'owner': self.owner,
      'game_id': self.game_id
    }