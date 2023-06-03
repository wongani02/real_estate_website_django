# Generated by Django 4.1.1 on 2023-04-22 18:04

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodges', '0006_about_blogcategory_blogpost_blogimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='about',
            name='about_text',
            field=ckeditor.fields.RichTextField(help_text='what is your company like? mission, values etc..', null=True),
        ),
    ]