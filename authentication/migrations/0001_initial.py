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
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(max_length=2, unique=True)),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
                'ordering': ['lang'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('manager', 'Manager'), ('client', 'Client'), ('consultant', 'Consultant')], default='client', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('date_of_birth', models.DateTimeField(blank=True, null=True, verbose_name='date of birth')),
                ('address', models.TextField(blank=True, null=True, verbose_name='address')),
                ('phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='phone number')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images', verbose_name='user photo')),
                ('note', models.TextField(blank=True, null=True)),
                ('enable', models.BooleanField(blank=True, null=True)),
                ('langs', models.ManyToManyField(blank=True, to='authentication.language', verbose_name='languages')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'UserProfile',
                'verbose_name_plural': 'UserProfiles',
                'ordering': ['-id'],
            },
        ),
    ]
