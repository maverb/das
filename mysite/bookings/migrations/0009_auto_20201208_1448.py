# Generated by Django 3.1.2 on 2020-12-08 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0008_auto_20201113_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='photo',
            field=models.ImageField(default='nogenderavatar.png', upload_to='images/'),
        ),
    ]
