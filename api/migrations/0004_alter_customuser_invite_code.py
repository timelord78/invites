# Generated by Django 4.0.3 on 2022-03-21 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_customuser_is_staff_customuser_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='invite_code',
            field=models.CharField(max_length=6, unique=True),
        ),
    ]
