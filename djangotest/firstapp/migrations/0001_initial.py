# Generated by Django 5.1.7 on 2025-04-17 05:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bio', models.TextField()),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('nationality', models.CharField(max_length=50)),
                ('awards', models.TextField(blank=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='actors/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CensorInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(choices=[('G', 'General Audiences'), ('PG', 'Parental Guidance'), ('PG-13', 'Parents Strongly Cautioned'), ('R', 'Restricted'), ('NC-17', 'Adults Only')], max_length=5)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Censor Information',
                'verbose_name_plural': 'Censor Information',
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bio', models.TextField()),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('nationality', models.CharField(max_length=50)),
                ('awards', models.TextField(blank=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='directors/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MovieInformationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('rating', models.CharField(max_length=10)),
                ('description', models.TextField()),
                ('poster', models.ImageField(upload_to='posters/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('actors', models.ManyToManyField(related_name='acted_movies', to='firstapp.actor')),
                ('censor_details', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movie', to='firstapp.censorinfo')),
                ('directed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='directed_movies', to='firstapp.director')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
