# Generated by Django 4.1.7 on 2023-04-11 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='matchdata',
            options={'ordering': ['match__event_id', 'match__level', 'match__num', 'id']},
        ),
        migrations.AlterModelOptions(
            name='superscout',
            options={'ordering': ['match__event_id', 'match__level', 'match__num', 'id']},
        ),
        migrations.AlterModelOptions(
            name='systemscoring',
            options={'ordering': ['match__event_id', 'match__level', 'match__num', 'id']},
        ),
        migrations.RemoveField(
            model_name='superscout',
            name='other',
        ),
        migrations.AddField(
            model_name='matchdata',
            name='played',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='matchdata',
            name='tele_pick_db',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='matchdata',
            name='tele_pick_dn',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='superscout',
            name='comment',
            field=models.TextField(default='', null=True),
        ),
        migrations.AddField(
            model_name='superscout',
            name='dodge',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='matchdata',
            name='auto_grid',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='matchdata',
            name='other_comment',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='matchdata',
            name='other_link',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='matchdata',
            name='scouter',
            field=models.CharField(default='', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='matchdata',
            name='tele_defender',
            field=models.CharField(default='', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='matchdata',
            name='tele_grid',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='matchdata',
            name='timer_cycle',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='matchdata',
            name='timer_dock',
            field=models.TextField(default='', null=True),
        ),
    ]
