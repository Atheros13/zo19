# Generated by Django 2.2.4 on 2019-12-27 03:25

from django.db import migrations, models
import zo.custom.model_fields_draft.distancefield


class Migration(migrations.Migration):

    dependencies = [
        ('zo', '0007_auto_20191127_1313'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', zo.custom.model_fields_draft.distancefield.DistanceField()),
            ],
        ),
    ]
