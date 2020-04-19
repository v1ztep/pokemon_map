# Generated by Django 2.2.3 on 2020-04-19 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0002_auto_20200419_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entities', to='pokemon_entities.Pokemon', verbose_name='Название покемона'),
        ),
    ]
