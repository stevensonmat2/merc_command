from django.db import models
import uuid


class ComponentProfile(models.Model):
    name = models.CharField(max_length=30)


class WeaponProfile(models.Model):
    name = models.CharField(max_length=30)


class BattleMechProfile(models.Model):
    name = models.CharField(max_length=30)
