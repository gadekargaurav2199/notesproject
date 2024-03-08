from django.db import models

# Create your models here.
class PDF(models.Model):
    Publication_id=models.BigIntegerField(null=True)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='pdfs/')
    cover_image = models.FileField(upload_to='cover image/',null=True)
    desc = models.CharField(max_length=1000,null=True)
    date=models.DateField(null=True)
    
class Publication_user(models.Model):
    Publication_Name=models.CharField(max_length=100)
    profile=models.FileField(upload_to='profile/')
    description=models.CharField(max_length=1000)
    email=models.EmailField()
    password=models.CharField(max_length=500)
    DOC=models.DateField()



class advertisement(models.Model):
    Store_Name=models.CharField(max_length=1000)
    Store_Address=models.CharField(max_length=1000)
    banner=models.FileField(upload_to='advertisement_banner/')
    location=models.CharField(max_length=250)
    date=models.DateField()

