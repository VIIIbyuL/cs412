# Generated by Django 5.1.3 on 2024-12-09 20:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_app', '0003_alter_pokedex_base_exp'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('profile_pfp', models.URLField()),
                ('joined_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemon_app.profile'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='proposer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemon_app.profile'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
