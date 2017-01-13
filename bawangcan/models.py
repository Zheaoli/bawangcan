from django.db import models


# Create your models here.
class User(models.Model):
    user_name = models.CharField(blank=False, null=False, max_length=255)
    user_email = models.CharField(blank=False, null=False, max_length=255)
    user_password = models.CharField(blank=False, null=False, max_length=255)
    user_id = models.CharField(blank=False, null=False, max_length=255, unique=True)
    user_money = models.IntegerField(blank=False, null=False)


class BawangcanActivity(models.Model):
    activity_time = models.CharField(blank=False, null=False, max_length=255)
    activity_type = models.IntegerField(blank=False, null=False)
    activity_id = models.CharField(blank=False, null=False, max_length=255, unique=True)


class BawangcanStatus(models.Model):
    status_activity_id = models.CharField(blank=False, null=False, max_length=255)
    status_start_time = models.IntegerField(blank=False, null=False)
    status_end_time = models.IntegerField(blank=False, null=True)
    status_count = models.IntegerField(blank=False, null=False)
    status_status = models.IntegerField(blank=False, null=False)
    status_type = models.IntegerField(blank=False, null=False)


class BawangcanRecord(models.Model):
    record_activity_id = models.CharField(blank=False, null=False, max_length=255)
    record_create_time = models.IntegerField(blank=False, null=False)
    record_user_id = models.CharField(blank=False, null=False, max_length=255)

class BawangcanAward(models.Model):
    award_id = models.CharField(blank=False, null=False, max_length=255)
    award_user_id = models.CharField(blank=False, null=False, max_length=255)
    award_activity_id = models.CharField(blank=False, null=False, max_length=255)
    award_time = models.IntegerField(blank=False, null=False)
