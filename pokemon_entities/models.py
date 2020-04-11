from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    Lat = models.FloatField()
    Lon = models.FloatField()
    # Pokemon = models.ForeignKey(Pokemon, on_delete=models.SET_NULL)
