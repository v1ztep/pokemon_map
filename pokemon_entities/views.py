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

    pokemon_entitys = PokemonEntity.objects.filter(pokemon__id=pokemon_id)

    pokemon = []
    for pokemon_entity in pokemon_entitys:
        previous_evolution = ''
        if Pokemon.objects.filter(title=pokemon_entity.pokemon.previous_evolution).count() > 0:
            previous_evolution = {
                "title_ru": pokemon_entity.pokemon.previous_evolution.title,
                "pokemon_id": pokemon_entity.pokemon.previous_evolution.id,
                "img_url": request.build_absolute_uri(pokemon_entity.pokemon.previous_evolution.image.url)
            }

        next_evolution = ''
        if pokemon_entity.pokemon.next_evolutions.all().count() > 0:
            next_evolution = {
                "title_ru": pokemon_entity.pokemon.next_evolutions.first().title,
                "pokemon_id": pokemon_entity.pokemon.next_evolutions.first().id,
                "img_url": request.build_absolute_uri(pokemon_entity.pokemon.next_evolutions.first().image.url)
            }

        pokemon.append({
            "pokemon_id": pokemon_entity.pokemon.id,
            "title_ru": pokemon_entity.pokemon.title,
            "title_en": pokemon_entity.pokemon.title_en,
            "title_jp": pokemon_entity.pokemon.title_jp,
            "description": pokemon_entity.pokemon.description,
            "img_url": request.build_absolute_uri(pokemon_entity.pokemon.image.url),
            "previous_evolution": previous_evolution,
            "next_evolution": next_evolution
        })
        break

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entitys:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title, request.build_absolute_uri(pokemon_entity.pokemon.image.url))

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon[0]})
