# Generated by Django 5.1.5 on 2025-01-22 16:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('type', models.CharField(choices=[('todo_list', 'Todo List'), ('movie', 'Movie'), ('tv_show', 'TV Show'), ('anime', 'Anime')], max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_id', models.IntegerField(null=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('user_note', models.TextField(blank=True)),
                ('image', models.URLField(blank=True)),
                ('user_grade', models.IntegerField(null=True)),
                ('grade', models.FloatField(null=True)),
                ('release_year', models.IntegerField(null=True)),
                ('complete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('additional_info', models.JSONField(null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='app.category')),
            ],
        ),
    ]
