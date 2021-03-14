# Generated by Django 3.1.2 on 2020-10-27 18:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_auto_20201026_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='artist',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bookings.artist'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='offer',
            name='date',
            field=models.DateField(verbose_name='day of the party'),
        ),
    ]
