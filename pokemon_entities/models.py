from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(blank=True)
    title_en = models.CharField(max_length=20, blank=True)
    title_jp = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    Pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    Lat = models.FloatField()
    Lon = models.FloatField()

    Appeared_at = models.DateTimeField(null=True, blank=True)
    Disappeared_at = models.DateTimeField(null=True, blank=True)

    Level = models.IntegerField(null=True, blank=True)
    Health = models.IntegerField(null=True, blank=True)
    Strength = models.IntegerField(null=True, blank=True)
    Defence = models.IntegerField(null=True, blank=True)
    Stamina = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.Lat}, {self.Lon}, {self.Pokemon}'
