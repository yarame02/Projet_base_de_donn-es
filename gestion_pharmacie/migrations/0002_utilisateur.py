# Generated by Django 5.0.2 on 2024-08-22 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_pharmacie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_utilisateur', models.CharField(max_length=100)),
                ('mot_de_passe', models.CharField(max_length=100)),
            ],
        ),
    ]
