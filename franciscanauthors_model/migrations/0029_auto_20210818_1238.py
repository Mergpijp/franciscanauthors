# Generated by Django 3.1.12 on 2021-08-18 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('franciscanauthors_model', '0028_auto_20210727_1723'),
    ]

    operations = [
        migrations.RenameField(
            model_name='literature',
            old_name='add_comments',
            new_name='lit_text',
        ),
    ]