# Generated by Django 3.1.7 on 2021-04-14 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0015_auto_20210415_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_entities', to='pokemon_entities.pokemon', verbose_name='Покемон'),
        ),
    ]
