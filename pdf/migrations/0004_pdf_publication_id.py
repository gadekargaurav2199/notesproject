# Generated by Django 4.2.2 on 2024-01-28 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0003_rename_user_publication_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdf',
            name='Publication_id',
            field=models.BigIntegerField(null=True),
        ),
    ]
