# Generated by Django 4.2.1 on 2023-06-07 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_user_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_code',
            field=models.CharField(default='USER8340792023', editable=False, max_length=20, unique=True),
        ),
    ]
