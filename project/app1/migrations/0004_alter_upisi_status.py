# Generated by Django 4.0.5 on 2022-06-19 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_upisi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upisi',
            name='status',
            field=models.CharField(choices=[('up', 'upisan'), ('pol', 'polozen'), ('izg', 'izgubio potpis')], default='up', max_length=50),
        ),
    ]