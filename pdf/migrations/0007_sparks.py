# Generated by Django 4.2.2 on 2024-04-11 16:21

from django.db import migrations, models
import pdf.models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0006_alter_advertisement_banner_alter_pdf_cover_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='sparks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Publication_id', models.BigIntegerField(null=True)),
                ('title', models.CharField(max_length=100)),
                ('file', models.FileField(storage=pdf.models.PDFStorage(), upload_to='sparks/')),
                ('desc', models.CharField(max_length=1000, null=True)),
                ('date', models.DateField(null=True)),
            ],
        ),
    ]
