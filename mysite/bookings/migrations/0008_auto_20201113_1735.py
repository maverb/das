# Generated by Django 3.1.2 on 2020-11-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0007_artist_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
