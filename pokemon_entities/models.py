from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название покемона на русском')
    image = models.ImageField(null=True, blank=True, verbose_name='Картинка')
    description = models.TextField(blank=True, verbose_name='Описание')
    title_en = models.CharField(max_length=20, blank=True, verbose_name='Имя покемона на английском')
    title_jp = models.CharField(max_length=20, blank=True, verbose_name='имя покемона на японском')
    previous_evolution = models.ForeignKey("self", on_delete=models.SET_NULL,
                                           related_name='next_evolutions',
                                           null=True, blank=True,
                                           verbose_name='Из кого эволюционирует')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    Pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Название покемона')

    Lat = models.FloatField(verbose_name='Широта')
    Lon = models.FloatField(verbose_name='Долгота')

    Appeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Появится в')
    Disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Исчезнет в')

    Level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    Health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    Strength = models.IntegerField(null=True, blank=True, verbose_name='Сила')
    Defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    Stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')

    def __str__(self):
        return f'{self.Lat}, {self.Lon}, {self.Pokemon}'
