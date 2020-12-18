# Generated by Django 3.0 on 2020-12-17 23:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='TavvyCat', max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Mango',
        ),
        migrations.AddField(
            model_name='game',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
