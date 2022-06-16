# Generated by Django 4.0.3 on 2022-06-16 08:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('finish', models.DateTimeField()),
                ('length', models.PositiveIntegerField(default=0)),
                ('lengthHM', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Sleep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locked', models.BooleanField(default=False)),
                ('note', models.TextField(blank=True, default='', null=True)),
                ('startRoutineTime', models.DateTimeField()),
                ('startFallingAsleepTime', models.DateTimeField()),
                ('finishTime', models.DateTimeField()),
                ('isItNightSleep', models.BooleanField(default=False)),
                ('place', models.CharField(blank=True, max_length=255, null=True)),
                ('moodStartOfSleep', models.CharField(blank=True, max_length=255, null=True)),
                ('moodEndOfSleep', models.CharField(blank=True, max_length=255, null=True)),
                ('segments', models.ManyToManyField(blank=True, to='storage.segment')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=200)),
                ('birthdate', models.DateTimeField(blank=True, null=True)),
                ('createdAt', models.DateTimeField(blank=True, null=True)),
                ('consultant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('sleeps', models.ManyToManyField(blank=True, to='storage.sleep')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
    ]
