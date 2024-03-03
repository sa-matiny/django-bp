from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.contrib.auth.models import User


def validate_rate_range(value):
  if value > 5 or value < 0:
    raise ValidationError('is not between 0 - 5')

# Create your models here.
class Post(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=255)
  content = models.TextField(blank=True, null=True)

  def __str__(self):
    return f"id:{self.id} - title:{self.title}"

class Rating(models.Model):
  id = models.AutoField(primary_key=True)
  user_id = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
  post_id = models.ForeignKey(Post, related_name='ratings', on_delete=models.CASCADE)
  rate = models.IntegerField(validators=[validate_rate_range])

  def __str__(self):
    return f"post_id:{self.post_id} - rate:{self.rate}"

  class Meta:
    unique_together = ("user_id", "post_id")


