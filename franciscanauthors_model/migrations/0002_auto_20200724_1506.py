# Generated by Django 3.0.8 on 2020-07-24 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('franciscanauthors_model', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Editions_Translations',
            new_name='Edition_Translation',
        ),
        migrations.RenameModel(
            old_name='Manuscript_Editions',
            new_name='Manuscript_Edition',
        ),
        migrations.RenameModel(
            old_name='Translations',
            new_name='Translation',
        ),
        migrations.RemoveField(
            model_name='record',
            name='editions',
        ),
        migrations.AddField(
            model_name='record',
            name='editions',
            field=models.ManyToManyField(to='franciscanauthors_model.Editions'),
        ),
        migrations.RemoveField(
            model_name='record',
            name='editions_translations',
        ),
        migrations.AddField(
            model_name='record',
            name='editions_translations',
            field=models.ManyToManyField(to='franciscanauthors_model.Edition_Translation'),
        ),
        migrations.RemoveField(
            model_name='record',
            name='manuscripts',
        ),
        migrations.AddField(
            model_name='record',
            name='manuscripts',
            field=models.ManyToManyField(to='franciscanauthors_model.Manuscript'),
        ),
        migrations.RemoveField(
            model_name='record',
            name='manuscripts_editions',
        ),
        migrations.AddField(
            model_name='record',
            name='manuscripts_editions',
            field=models.ManyToManyField(to='franciscanauthors_model.Manuscript_Edition'),
        ),
        migrations.RemoveField(
            model_name='record',
            name='translations',
        ),
        migrations.AddField(
            model_name='record',
            name='translations',
            field=models.ManyToManyField(to='franciscanauthors_model.Translation'),
        ),
    ]
