# Generated by Django 4.1.4 on 2022-12-21 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_venue_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='venue_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
