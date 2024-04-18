from storages.backends.s3boto3 import S3Boto3Storage
from django.db import models

class PDFStorage(S3Boto3Storage):
    location = 'media'  # The folder in your S3 bucket where files will be stored

# Create your models here.
class PDF(models.Model):
    Publication_id=models.BigIntegerField(null=True)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='pdfs/', storage=PDFStorage())
    cover_image = models.FileField(upload_to='cover image/', storage=PDFStorage(), null=True)
    desc = models.CharField(max_length=1000,null=True)
    date=models.DateField(null=True)
    
class sparks(models.Model):
    Publication_id=models.BigIntegerField(null=True)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='sparks/', storage=PDFStorage())
    desc = models.CharField(max_length=1000,null=True)
    date=models.DateField(null=True)
    
class Publication_user(models.Model):
    Publication_Name=models.CharField(max_length=100)
    profile=models.FileField(upload_to='profile/', storage=PDFStorage(), null=True)
    description=models.CharField(max_length=1000)
    email=models.EmailField()
    password=models.CharField(max_length=500)
    DOC=models.DateField()

class advertisement(models.Model):
    Store_Name=models.CharField(max_length=1000)
    Store_Address=models.CharField(max_length=1000)
    banner=models.FileField(upload_to='advertisement_banner/',storage=PDFStorage(), null=True)
    location=models.CharField(max_length=250)
    date=models.DateField()

