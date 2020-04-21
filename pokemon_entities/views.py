import folium

from django.shortcuts import render, get_object_or_404
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
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title, request.build_absolute_uri(pokemon_entity.pokemon.image.url))

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
    get_object_or_404(Pokemon, id=pokemon_id)

    displayed_pokemon = Pokemon.objects.prefetch_related('previous_evolution', 'next_evolution').get(id=pokemon_id)
    pokemon_entities = displayed_pokemon.entities.all()

    pokemon = []

    previous_evolution = ''
    if displayed_pokemon.previous_evolution:
        previous_evolution = {
            "title_ru": displayed_pokemon.previous_evolution.title,
            "pokemon_id": displayed_pokemon.previous_evolution.id,
            "img_url": request.build_absolute_uri(displayed_pokemon.previous_evolution.image.url)
        }

    next_evolution = ''
    if displayed_pokemon.next_evolution.exists():
        next_evolution_pokemon = displayed_pokemon.next_evolution.all()[0]
        next_evolution = {
            "title_ru": next_evolution_pokemon.title,
            "pokemon_id": next_evolution_pokemon.id,
            "img_url": request.build_absolute_uri(next_evolution_pokemon.image.url)
        }

    pokemon.append({
        "pokemon_id": displayed_pokemon.id,
        "title_ru": displayed_pokemon.title,
        "title_en": displayed_pokemon.title_en,
        "title_jp": displayed_pokemon.title_jp,
        "description": displayed_pokemon.description,
        "img_url": request.build_absolute_uri(displayed_pokemon.image.url),
        "previous_evolution": previous_evolution,
        "next_evolution": next_evolution
    })

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title, request.build_absolute_uri(pokemon_entity.pokemon.image.url))

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon[0]})
