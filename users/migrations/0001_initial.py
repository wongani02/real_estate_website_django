# Generated by Django 4.1.1 on 2023-03-05 23:10

import ckeditor.fields
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Client ID')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Client Username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='CLient Email Address')),
                ('name', models.CharField(blank=True, max_length=40, verbose_name='Client Full Name')),
                ('is_realtor', models.BooleanField(default=False, verbose_name='If user is a realtor set it to True')),
                ('is_customer', models.BooleanField(default=False, verbose_name='If user is a customer set it to True')),
                ('is_active', models.BooleanField(default=False, verbose_name='If user is active set it to True')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', ckeditor.fields.RichTextField(null=True)),
                ('profile_img', models.ImageField(blank=True, help_text='Profile image', null=True, upload_to='profile_imgs')),
                ('phone_number', models.CharField(blank=True, help_text='phone number', max_length=10, null=True)),
                ('agency_certificate', models.FileField(blank=True, help_text='agency certificates', null=True, upload_to='agency_certificates')),
                ('realtor_cretificate', models.FileField(blank=True, help_text='realtor certificates', null=True, upload_to='realtor_certificates')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]