# Generated by Django 2.1.2 on 2018-10-28 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_auto_20181028_0250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamemodel',
            name='winning_player',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
