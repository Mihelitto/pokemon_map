import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon
from pokemon_entities.models import PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, pokemon_entitie, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [pokemon_entitie.lat, pokemon_entitie.lon],
        # Warning! `tooltip` attribute is disabled intentionally to fix strange folium cyrillic encoding bug
        popup=folium.Popup(
            f"<center><b>L</b> - {pokemon_entitie.level}<center>\
             <p><b>H</b> - {pokemon_entitie.health} |\
             <b>St</b> - {pokemon_entitie.stamina}</p>\
             <p><b>S</b> - {pokemon_entitie.strength} |\
             <b>D</b> - {pokemon_entitie.defence}\
             </p>",
            max_width=120),
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    if pokemon.previous_evolution:
        previous_evolution = {
            "title_ru": pokemon.previous_evolution.title,
            "pokemon_id": pokemon.previous_evolution.id,
            "img_url": request.build_absolute_uri(pokemon.previous_evolution.image.url),
        }
    else:
        previous_evolution = None

    related_pokemon = pokemon.next_evolutions.first()
    if related_pokemon:
        next_evolution = {
            "title_ru": related_pokemon.title,
            "pokemon_id": related_pokemon.id,
            "img_url": request.build_absolute_uri(related_pokemon.image.url),
        }
    else:
        next_evolution = None

    if pokemon.element_type.all():
        element_types = list()
        for element in pokemon.element_type.all():
            element_types.append({
                "title": element.title,
                "img": request.build_absolute_uri(element.image.url),
                "strong_against": element.strong_against.all(),
            })
    else:
        element_types = None

    pokemon_properties = {
        "title_ru": pokemon.title,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "img_url": request.build_absolute_uri(pokemon.image.url),
        "pokemon_id": pokemon.id,
        "description": pokemon.description,
        "previous_evolution": previous_evolution,
        "next_evolution": next_evolution,
        "element_type": element_types,
    }
    pokemon_entities = pokemon.pokemon_entities.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_properties})
