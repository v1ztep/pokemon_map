from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    Pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    Lat = models.FloatField()
    Lon = models.FloatField()

    Appeared_at = models.DateTimeField(default=None)
    Disappeared_at = models.DateTimeField(default=None)

    Level = models.IntegerField(default=None)
    Health = models.IntegerField(default=None)
    Strength = models.IntegerField(default=None)
    Defence = models.IntegerField(default=None)
    Stamina = models.IntegerField(default=None)
