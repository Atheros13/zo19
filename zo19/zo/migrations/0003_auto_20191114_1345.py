# Generated by Django 2.2.4 on 2019-11-14 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zo', '0002_userpasswordreset'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rankgroup',
            name='type',
        ),
        migrations.AddField(
            model_name='rank',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='rankgroup',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='rankgroup',
            name='types',
            field=models.ManyToManyField(related_name='rank_groups', to='zo.RankGroupType'),
        ),
        migrations.AddField(
            model_name='rankgrouptype',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='agegrade',
            name='open',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='agegrade',
            name='under',
            field=models.NullBooleanField(default=True),
        ),
    ]
