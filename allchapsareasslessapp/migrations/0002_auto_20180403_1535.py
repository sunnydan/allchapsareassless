# Generated by Django 2.0.3 on 2018-04-03 19:35

import allchapsareasslessapp.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('allchapsareasslessapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='cards/')),
                ('bonusCard', models.BooleanField(default=False)),
                ('private', models.BooleanField(default=False)),
                ('dateCreated', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=30)),
                ('description', models.TextField(max_length=255)),
                ('private', models.BooleanField(default=False)),
                ('dateCreated', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=30)),
                ('cards', models.ManyToManyField(related_name='tags', to='allchapsareasslessapp.Card')),
                ('decks', models.ManyToManyField(related_name='tags', to='allchapsareasslessapp.Deck')),
            ],
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', allchapsareasslessapp.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='settings.MEDIA_ROOT/avatars/default.png', upload_to='avatars/'),
        ),
        migrations.AddField(
            model_name='user',
            name='gamesPlayed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='gamesWon',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='memberSince',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='user',
            name='roundsWon',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='displayName',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AddField(
            model_name='deck',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='decks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='deck',
            name='cards',
            field=models.ManyToManyField(related_name='decks', to='allchapsareasslessapp.Card'),
        ),
        migrations.AddField(
            model_name='deck',
            name='likingUsers',
            field=models.ManyToManyField(related_name='likedDecks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='card',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='card',
            name='likingUsers',
            field=models.ManyToManyField(related_name='likedCards', to=settings.AUTH_USER_MODEL),
        ),
    ]