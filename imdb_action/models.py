from django.db import models

# Create your models here.
class MovieStore(models.Model):
    name = models.TextField(blank=True, null=True)
    imdb_score = models.FloatField(blank=True, null=True)
    director = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    number_99popularity = models.FloatField(db_column='99popularity', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.

    class Meta:
        managed = False
        db_table = 'movie_store'

class AdminData(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=45)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'admin_data'

class UserData(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_data'