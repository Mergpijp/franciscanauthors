# Generated by Django 3.0.8 on 2021-03-03 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('franciscanauthors_model', '0011_auto_20210303_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='birth_date_precision_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='birth_dates', to='franciscanauthors_model.Date_precision'),
        ),
        migrations.AlterField(
            model_name='author',
            name='death_date_precision_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='death_dates', to='franciscanauthors_model.Date_precision'),
        ),
    ]
