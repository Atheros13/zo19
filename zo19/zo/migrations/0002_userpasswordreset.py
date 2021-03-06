# Generated by Django 2.2.4 on 2019-11-06 00:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPasswordReset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('random', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
