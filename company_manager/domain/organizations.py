from django.db import models
from django.contrib.auth.models import AbstractUser

REPAIR_COST = 10

ORIGIN_CHOICES = [
    ("CLAN", "Clan"),
    ("INNERSPHERE", "Inner-Sphere"),
]

FACTION_CHOICES = [()]


class User(AbstractUser):
    pass


class Faction(models.Model):
    origin = models.CharField(choices=ORIGIN_CHOICES)
    pass


class Company(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    origin = models.CharField(choices=ORIGIN_CHOICES)
    wallet = models.DecimalField(default=0, max_digits=12, decimal_places=2)


class FactionAffinity(models.Model):
    faction = models.ForeignKey(
        Faction, on_delete=models.CASCADE, related_name="affinities"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="affinities"
    )
    affinity = models.IntegerField(default=0)


class Contract(models.Model):
    offering_faction = models.ForeignKey(
        Faction, on_delete=models.CASCADE, related_name="contracts"
    )
    target_faction = models.ForeignKey(
        Faction, on_delete=models.CASCADE, related_name="contracts"
    )
    contracted_company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
    )
    base_pay = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
