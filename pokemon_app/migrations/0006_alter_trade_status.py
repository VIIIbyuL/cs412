# Generated by Django 5.1.3 on 2024-12-10 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_app', '0005_trade_receiver_alter_trade_proposer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='status',
            field=models.CharField(choices=[('in_progress', 'In Progress'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='in_progress', max_length=12),
        ),
    ]
