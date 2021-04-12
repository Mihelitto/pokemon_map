from django.db import models


class Pokemon(models.Model):
    title = models.CharField("Название", max_length=200)
    title_en = models.CharField("Название на английском", max_length=200, default="")
    title_jp = models.CharField("Название на японском", max_length=200, default="")
    image = models.ImageField("Изображение", upload_to="pokemons", blank=True, null=True)
    description = models.TextField("Описание", max_length=500, blank=True, null=True)
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
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

    appeared_at = models.DateTimeField("Появился")
    disappeared_at = models.DateTimeField("Исчезнет")

    level = models.IntegerField("Уровень")
    health = models.IntegerField("Здоровье")
    strength = models.IntegerField("Сила")
    defence = models.IntegerField("Защита")
    stamina = models.IntegerField("Выносливость")

    def __str__(self):
        return f"{self.pokemon.title}: появился - {self.appeared_at.strftime('%Y-%m-%d-%H.%M.%S')}"

    class Meta:
        verbose_name = "Сущность покемона"
        verbose_name_plural = "Сущности покемонов"