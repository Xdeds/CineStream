# Generated by Django 4.2.3 on 2023-08-22 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_alter_actor_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='raitingstar',
            options={'ordering': ['-value'], 'verbose_name': 'Звезда рейтинга', 'verbose_name_plural': 'Звезды рейтинга'},
        ),
    ]
