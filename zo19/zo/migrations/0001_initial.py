# Generated by Django 2.2.4 on 2019-10-24 20:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import djangoyearlessdate.models
import zo.models.user


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('dob', models.DateField(null=True)),
                ('phone_number', models.CharField(blank=True, max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_authorised', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', zo.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AgeGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open', models.BooleanField(default=False)),
                ('under', models.BooleanField(default=True)),
                ('age', models.PositiveIntegerField(blank=True)),
                ('date', djangoyearlessdate.models.YearlessDateField(blank=True, max_length=4)),
            ],
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RankGroupType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='UserSignUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(blank=True)),
                ('is_staff', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserHubSignUp',
            fields=[
                ('usersignup_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='zo.UserSignUp')),
                ('hub_name', models.CharField(max_length=30)),
                ('hub_phone', models.CharField(max_length=30)),
                ('hub_street', models.CharField(max_length=50)),
                ('hub_towncity', models.CharField(max_length=50)),
            ],
            bases=('zo.usersignup',),
        ),
        migrations.CreateModel(
            name='UserTemporaryPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temporary_password', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50, verbose_name='First Name')),
                ('middlenames', models.CharField(blank=True, max_length=50, verbose_name='Middle Name/s')),
                ('surname', models.CharField(max_length=30)),
                ('preferred_name', models.CharField(blank=True, default='', max_length=50, verbose_name='Preferred Name')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='name', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line1', models.CharField(max_length=50, verbose_name='Address Line 1')),
                ('line2', models.CharField(blank=True, max_length=50, verbose_name='Address Line 2')),
                ('line3', models.CharField(blank=True, max_length=50, verbose_name='Address Line 3')),
                ('town_city', models.CharField(max_length=50, verbose_name='Town/City')),
                ('postcode', models.CharField(blank=True, max_length=50, verbose_name='Postcode')),
                ('country', models.CharField(blank=True, max_length=50, verbose_name='Country')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RankGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rank_groups', to='zo.RankGroupType')),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('rank_value', models.PositiveIntegerField(blank=True)),
                ('rank_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ranks', to='zo.RankGroup')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='zo.AgeGrade')),
                ('genders', models.ManyToManyField(related_name='grades', to='zo.Gender')),
                ('ranks', models.ManyToManyField(related_name='grades', to='zo.Rank')),
            ],
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='zo.Gender'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='HubSignUp',
            fields=[
                ('userhubsignup_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='zo.UserHubSignUp')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('zo.userhubsignup',),
        ),
    ]
