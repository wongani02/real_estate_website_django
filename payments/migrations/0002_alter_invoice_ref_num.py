# Generated by Django 4.1.1 on 2023-03-08 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='ref_num',
            field=models.CharField(default='97305d3d214d', max_length=12, null=True),
        ),
    ]