from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from constants import ORIGIN_CHOICES


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=30)


class Faction(models.Model):
    origin = models.CharField(max_length=30, choices=ORIGIN_CHOICES)
    pass


class Company(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="companies"
    )
    origin = models.CharField(max_length=30, choices=ORIGIN_CHOICES)
    wallet = models.DecimalField(default=0, max_digits=12, decimal_places=2)


class FactionAffinity(models.Model):
    faction = models.ForeignKey(
        Faction, on_delete=models.CASCADE, related_name="faction_affinities"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_affinities"
    )
    affinity = models.IntegerField(default=0)


class Contract(models.Model):
    offering_faction = models.ForeignKey(
        Faction, on_delete=models.CASCADE, related_name="offering_contracts"
    )
    target_faction = models.ForeignKey(
        Faction, on_delete=models.CASCADE, related_name="target_contracts"
    )
    contracted_company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
    )
    base_pay = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
