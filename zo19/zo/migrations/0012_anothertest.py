# Generated by Django 2.2.4 on 2019-12-31 08:20

from django.db import migrations, models
import zo.custom.model_fields.custom_distance


class Migration(migrations.Migration):

    dependencies = [
        ('zo', '0011_delete_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnotherTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', zo.custom.model_fields.custom_distance.CustomDistanceField(max_length=100)),
            ],
        ),
    ]
