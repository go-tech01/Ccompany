from django.db import models
from django.db.models import JSONField



# Create your models here.


class EstimateModel(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=13)
    area = models.IntegerField()
    TYPES = (('apt', '아파트'), ('house', '주택'), ('store', '상가'))
    types = models.CharField(max_length=50, choices=TYPES)
    input_estimateimage = models.ImageField(upload_to='input_estimate', null=False)


class Output(models.Model):
    list_11 = models.CharField(max_length=500)
    list_22 = JSONField()
    list_33 = JSONField()