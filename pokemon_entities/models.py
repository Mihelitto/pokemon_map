from django.db import models
from django.utils.timezone import now


class Pokemon(models.Model):
    title = models.CharField("Название", max_length=200)
    title_en = models.CharField("Название на английском", max_length=200, default="")
    title_jp = models.CharField("Название на японском", max_length=200, default="")
    image = models.ImageField("Изображение", upload_to="pokemons")
    description = models.TextField("Описание", max_length=500, default="")
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="next_evolutions",
        verbose_name="Из кого эволюционирует"
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Покемон"
        verbose_name_plural = "Покемоны"


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон")
    lat = models.FloatField("Широта")
    lon = models.FloatField("Долгота")

    appeared_at = models.DateTimeField("Появился", blank=True, null=True)
    disappeared_at = models.DateTimeField("Исчезнет", blank=True, null=True)

    level = models.IntegerField("Уровень", blank=True, null=True)
    health = models.IntegerField("Здоровье", blank=True, null=True)
    strength = models.IntegerField("Сила", blank=True, null=True)
    defence = models.IntegerField("Защита", blank=True, null=True)
    stamina = models.IntegerField("Выносливость", blank=True, null=True)

    def __str__(self):
        return f"{self.pokemon.title}({self.id})"

    class Meta:
        verbose_name = "Сущность покемона"
        verbose_name_plural = "Сущности покемонов"