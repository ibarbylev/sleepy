# Generated by Django 4.0.3 on 2022-06-14 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('storage', '0002_alter_client_options_alter_segment_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='consultant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='authentication.user'),
        ),
    ]
