# Generated by Django 4.1.7 on 2023-03-07 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_rename_tele_defended_matchdata_other_tippy_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='matchdata',
            old_name='target',
            new_name='match',
        ),
        migrations.RenameField(
            model_name='superscout',
            old_name='target',
            new_name='match',
        ),
    ]