# Generated by Django 2.2.3 on 2020-11-16 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0002_auto_20201115_2045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemonelementtype',
            name='pokemon',
        ),
    ]
