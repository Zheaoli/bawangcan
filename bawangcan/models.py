from django.db import models


# Create your models here.
class User(models.Model):
    user_name = models.CharField(blank=False, null=False, max_length=255)
    user_email = models.CharField(blank=False, null=False, max_length=255)
    user_password = models.CharField(blank=False, null=False, max_length=255)
    user_id = models.CharField(blank=False, null=False, max_length=255, unique=True)


class BawangcanActivity(models.Model):
    activity_time = models.CharField(blank=False, null=False, max_length=255)
    activity_type = models.IntegerField(blank=False, null=False)
    activity_id = models.CharField(blank=False, null=False, max_length=255)

class BawangcanRecord(models.Model)
    pass