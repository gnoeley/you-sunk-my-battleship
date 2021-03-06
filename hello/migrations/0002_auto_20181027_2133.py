# Generated by Django 2.1.2 on 2018-10-27 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dbsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1', models.CharField(max_length=100)),
                ('player2', models.CharField(max_length=100)),
                ('session_state', models.CharField(max_length=100)),
                ('player_1_state', models.CharField(max_length=100)),
                ('player_2_state', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='greeting',
            name='when',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date created'),
        ),
    ]
