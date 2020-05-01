from django.db import models

# Create your models here.


class MovieRoom(models.Model):
    MovieRoom_Name = models.TextField(max_length=64)
    Movie_ID = models.IntegerField()
    MovieRoom_playing = models.BooleanField()
    MovieRoom_timming = models.IntegerField()

class MovieUser(models.Model):
    user_name = models.TextField(max_length=64)
    token = models.TextField(max_length=256)
    user_status = models.BooleanField()
    movie_room = models.ForeignKey(MovieRoom, on_delete=models.PROTECT,null=True)