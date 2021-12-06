from django.db import models
from .organizations import Company
from django.core.validators import MinValueValidator, MaxValueValidator


class Employee(models.Model):
    ROLE_CHOICES = [
        ("MECHWARRIOR", "MechWarrior"),
        ("ADMIN", "Admin"),
        ("SUPPORT", "Support"),
        ("MECHANIC", "Mechanic"),
    ]
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    rank = models.CharField(max_length=30, choices=ROLE_CHOICES)
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="employees"
    )


class MechWarrior(Employee):
    piloting_skill = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(0)]
    )
    gunnery_skill = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(0)]
    )
    experience = models.IntegerField(default=0)
    max_health = models.IntegerField(default=5)
    current_health = models.IntegerField(default=5)


class Trait(models.Model):
    pass
