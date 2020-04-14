import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.all():
        add_pokemon(
            folium_map, pokemon_entity.Lat, pokemon_entity.Lon,
            pokemon_entity.Pokemon.title, request.build_absolute_uri(pokemon_entity.Pokemon.image.url))

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        if pokemon.image:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'title_ru': pokemon.title,
                'img_url': pokemon.image.url
            })
        else:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'title_ru': pokemon.title,
            })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    if Pokemon.objects.filter(id=pokemon_id).count() > 0:
        pokemon_entitys = PokemonEntity.objects.filter(Pokemon__id=pokemon_id)

        pokemon = []
        for pokemon_entity in pokemon_entitys:
            pokemon.append({
                "pokemon_id": pokemon_entity.Pokemon.id,
                "title_ru": pokemon_entity.Pokemon.title,
                "title_en": pokemon_entity.Pokemon.title_en,
                "title_jp": pokemon_entity.Pokemon.title_jp,
                "description": pokemon_entity.Pokemon.description,
                "img_url": request.build_absolute_uri(pokemon_entity.Pokemon.image.url),
                "entities": "",
                "next_evolution": ""
            })
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entitys:
        add_pokemon(
            folium_map, pokemon_entity.Lat, pokemon_entity.Lon,
            pokemon_entity.Pokemon.title, request.build_absolute_uri(pokemon_entity.Pokemon.image.url))

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon[0]})
