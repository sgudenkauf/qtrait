from django.db import models
from datetime import datetime
from django.utils import timezone


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    last_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    serviceID = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Feature(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    featureID = models.CharField(max_length=200)
    parentID = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name
