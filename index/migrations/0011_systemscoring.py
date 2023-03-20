# Generated by Django 4.1.7 on 2023-03-19 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0010_alter_matchdata_tele_pick'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemScoring',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
                ('red', models.BooleanField(default=False)),
                ('mobility', models.IntegerField(default=0)),
                ('grid', models.IntegerField(default=0)),
                ('charge', models.IntegerField(default=0)),
                ('penalty', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('rank', models.IntegerField(default=0)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.match')),
            ],
        ),
    ]