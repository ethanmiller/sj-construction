from django.db import models

class Entity(models.Model):
    name = models.CharField(max_length=255)

class SubType(models.Model):
    name = models.CharField(max_length=255)

class WorkDescription(models.Model):
    name = models.CharField(max_length=255)

class Permit(models.Model):
    location = models.CharField(max_length=255)
    parcel = models.CharField(max_length=255, blank=True)
    applicant = models.ForeignKey(Entity, related_name='permits_applied_for', null=True)
    owner = models.ForeignKey(Entity, related_name='permits_on_owned', null=True)
    contractor = models.ForeignKey(Entity, related_name='permits_worked', null=True)
    folder_num = models.CharField(max_length=255, blank=True)
    folder_desc = models.CharField(max_length=255, blank=True)
    folder_name = models.CharField(max_length=255, blank=True)
    subtype = models.ForeignKey(SubType, null=True)
    work_desc = models.ForeignKey(WorkDescription, null=True)
    approvals = models.CharField(max_length=255, blank=True)
    issued = models.DateField()
    dwelling_units = models.FloatField(default=0.0)
    valuation = models.FloatField(default=0.0)
    square_footage = models.FloatField(default=0.0)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default=37.3004182)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=-121.8761836)


