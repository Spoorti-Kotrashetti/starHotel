from django.db import models

# Create your models here.
class cust(models.Model):
    cust_name = models.CharField(max_length=100)
    cust_mail = models.CharField(max_length=100)
    cust_password = models.CharField(max_length=100)
