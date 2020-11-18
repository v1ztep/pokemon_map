import folium

from django.shortcuts import render, get_object_or_404
from .models import Pokemon, PokemonEntity
from transliterate import translit

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def convert_list_to_string(org_list, seperator=' '):

    return seperator.join(org_list)


def add_pokemon(folium_map, lat, lon, name, level, elements_type_list, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )

    if elements_type_list:
        elements_list = []
        for title, image_url in elements_type_list:
            elements_list.append(f'<p style="margin:0"><img src="{image_url}"/>'
                                 f'{translit(title, "ru", reversed=True)}</p>')
        elements_type_str = convert_list_to_string(elements_list)
    else:
        elements_type_str = ''

    folium.Marker(
        [lat, lon],
        tooltip=translit(name, 'ru', reversed=True)+":"+str(level)+"lvl.",
        popup="<p style='margin:5px'> <b>"+translit(name, 'ru', reversed=True)+":"+str(level)+"</b>"+f"_lvl_</p>"
              +elements_type_str,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.all():
        elements_type_list = []
        if pokemon_entity.pokemon.element_type.exists():
            for element_type in pokemon_entity.pokemon.element_type.all():
                title_and_image_url_list = [element_type.title, request.build_absolute_uri(element_type.image.url)]
                elements_type_list.append(title_and_image_url_list)

        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title, pokemon_entity.level, elements_type_list,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url))


    pokemons_on_page_list = []
    for pokemon in Pokemon.objects.all():
        if pokemon.image:
            pokemons_on_page_list.append({
                'pokemon_id': pokemon.id,
                'title_ru': pokemon.title,
                'img_url': pokemon.image.url
            })
        else:
            pokemons_on_page_list.append({
                'pokemon_id': pokemon.id,
                'title_ru': pokemon.title,
            })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page_list,
    })


def show_pokemon(request, pokemon_id):
    displayed_pokemon = get_object_or_404(Pokemon.objects.prefetch_related('previous_evolution', 'next_evolutions'),
                                          id=pokemon_id)
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
    if displayed_pokemon.next_evolutions.exists():
        next_evolution_pokemon = displayed_pokemon.next_evolutions.all()[0]
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
        elements_type_list = []
        if pokemon_entity.pokemon.element_type.exists():
            for element_type in pokemon_entity.pokemon.element_type.all():
                title_and_image_url_list = [element_type.title, request.build_absolute_uri(element_type.image.url)]
                elements_type_list.append(title_and_image_url_list)

        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title, pokemon_entity.level, elements_type_list,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url))

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon[0]})



    # python manage.py shell
    # from pokemon_entities.models import Pokemon, PokemonEntity
    # from transliterate import translit
    #
    # for pokemon_entity in PokemonEntity.objects.all():
    #     elements_type_title_and_image_url_list = []
    #     if pokemon_entity.pokemon.element_type.exists():
    #         for element_type in pokemon_entity.pokemon.element_type.all():
    #             title_and_image_url_list = [element_type.title, element_type.image.url]
    #             elements_type_title_and_image_url_list.append(title_and_image_url_list)










