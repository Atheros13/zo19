# Generated by Django 2.2.4 on 2019-11-22 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0003_auto_20191122_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hubgroupmembershipperiods',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='hubgrouprankmembershipperiod',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='hubgrouprolemembershipperiod',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='hubrankmembershipperiod',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='hubrolemembershipperiod',
            name='end_date',
            field=models.DateField(null=True),
        ),
    ]
