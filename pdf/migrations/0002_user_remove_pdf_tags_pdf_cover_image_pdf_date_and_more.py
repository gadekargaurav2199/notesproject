# Generated by Django 4.2.2 on 2024-01-28 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Publication_Name', models.CharField(max_length=100)),
                ('profile', models.FileField(upload_to='profile/')),
                ('description', models.CharField(max_length=1000)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=500)),
                ('DOC', models.DateField()),
            ],
        ),
        migrations.RemoveField(
            model_name='pdf',
            name='tags',
        ),
        migrations.AddField(
            model_name='pdf',
            name='cover_image',
            field=models.FileField(null=True, upload_to='cover image/'),
        ),
        migrations.AddField(
            model_name='pdf',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='pdf',
            name='desc',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
