# Generated by Django 4.2 on 2023-04-13 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_delete_subscription'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-created',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
    ]
