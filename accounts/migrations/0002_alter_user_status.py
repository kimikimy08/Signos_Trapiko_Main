# Generated by Django 4.0.4 on 2022-09-29 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Active'), (3, 'Inactive')], null=True),
        ),
    ]
