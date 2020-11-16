from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название покемона на русском')
    image = models.ImageField(null=True, blank=True, verbose_name='Картинка')
    description = models.TextField(default='', verbose_name='Описание')
    title_en = models.CharField(max_length=20, default='', verbose_name='Имя покемона на английском')
    title_jp = models.CharField(max_length=20, default='', verbose_name='Имя покемона на японском')
    previous_evolution = models.ForeignKey("self", on_delete=models.SET_NULL,
                                           related_name='next_evolutions',
                                           null=True, blank=True,
                                           verbose_name='Из кого эволюционирует')

    element_type = models.ManyToManyField("PokemonElementType", related_name='elements', verbose_name='Стихия покемона')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE,
                                related_name='entities', verbose_name='Название покемона')

    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')

    appeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Появится в')
    disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Исчезнет в')

    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Сила')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')

    def __str__(self):
        return f'{self.lat}, {self.lon}, {self.pokemon}'


class PokemonElementType(models.Model):
    title = models.CharField(max_length=20, verbose_name='Стихия')

    def __str__(self):
        return self.title
