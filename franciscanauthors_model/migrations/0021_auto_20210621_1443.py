# Generated by Django 3.1.12 on 2021-06-21 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('franciscanauthors_model', '0020_auto_20210616_1542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='birth_date_precision_id',
            new_name='birth_date_precision',
        ),
        migrations.RenameField(
            model_name='author',
            old_name='death_date_precision_id',
            new_name='death_date_precision',
        ),
        migrations.RenameField(
            model_name='location_time',
            old_name='author_id',
            new_name='author',
        ),
        migrations.RemoveField(
            model_name='additional_info',
            name='author_id',
        ),
        migrations.RemoveField(
            model_name='alias',
            name='author_id',
        ),
        migrations.RemoveField(
            model_name='genre_group',
            name='genre_id',
        ),
        migrations.RemoveField(
            model_name='works',
            name='author_id',
        ),
        migrations.RemoveField(
            model_name='works',
            name='date_precision_id',
        ),
        migrations.RemoveField(
            model_name='works',
            name='genre_id',
        ),
        migrations.AddField(
            model_name='additional_info',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='additional_info_list', to='franciscanauthors_model.author'),
        ),
        migrations.AddField(
            model_name='alias',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alias_list', to='franciscanauthors_model.author'),
        ),
        migrations.AddField(
            model_name='genre_group',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='genre_group_list', to='franciscanauthors_model.genre'),
        ),
        migrations.AddField(
            model_name='works',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='works_author_list', to='franciscanauthors_model.author'),
        ),
        migrations.AddField(
            model_name='works',
            name='date_precision',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='works_date_list', to='franciscanauthors_model.date_precision'),
        ),
        migrations.AddField(
            model_name='works',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='works_genre_list', to='franciscanauthors_model.genre'),
        ),
    ]