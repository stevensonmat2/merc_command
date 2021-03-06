# from audioop import reverse
from django.urls import reverse
from django.db import models
from .organizations import Company
from .base import BaseModel
from .constants import REPAIR_COST, ORIGIN_CHOICES, MAINTENANCE_RATE
import uuid


class Equipment(BaseModel):
    variant = models.CharField(max_length=30, null=True, blank=True)
    production_year = models.IntegerField(null=True, blank=True)
    value = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    weight_tons = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="equipment",
        null=True,
        blank=True,
    )
    origin = models.CharField(
        max_length=30, choices=ORIGIN_CHOICES, null=True, blank=True
    )

    def build_equipment(self, equipment_profile):
        self.name = equipment_profile.get("name", "")
        self.variant = equipment_profile.get("variant", "")
        self.value = equipment_profile.get("value", 0.0)
        self.weight_tons = equipment_profile.get("weight", 0.0)
        self.save()

    def __str__(self):
        return self.name or str(self.id)


class ComplexEquipment(Equipment):
    def maintenance_upkeep(self):
        return self.value / MAINTENANCE_RATE


class DropShip(ComplexEquipment):
    mech_capacity = models.IntegerField()
    weight_limit = models.IntegerField()
    reliability = models.IntegerField()


class BattleMechDesign(ComplexEquipment):
    meta_data = models.JSONField(null=True, blank=True)
    designation = models.CharField(max_length=30, unique=False)


class BattleMech(ComplexEquipment):
    meta_data = models.TextField()
    designation = models.CharField(max_length=30, unique=False)

    def build_mech(self, mech_profile):
        self.build_segments(mech_profile["segments"])
        self.build_equipment(mech_profile)
        self.save()

    def build_segments(self, segments_profile):
        for segment in segments_profile:
            new_segment = Segment.objects.create(mech=self)
            new_segment.build_segment(segments_profile[segment])

    def update(self, mech_profile):
        self.build_segments(mech_profile)

    def total_repair_cost(self):
        repair_cost = 0
        segments = self.segments
        for segment in segments:
            repair_cost += segment.repair_cost()
        return repair_cost

    def view(self):
        return reverse("mech_view", kwargs={"pk": self.pk})


class Segment(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=30)
    SEGMENT_NAME_CHOICES = [
        ("HEAD", "Head"),
        ("CT", "Center Torso"),
        ("CTR", "Center Torso (Rear)"),
        ("LT", "Left Torso"),
        ("LTR", "Left Torso (Rear)"),
        ("RT", "Right Torso"),
        ("RTR", "Right Torso (Rear)"),
        ("LT", "Left Torso"),
        ("LA", "Left Arm"),
        ("RA", "Right Arm"),
        ("LL", "Left Leg"),
        ("RL", "Right Leg"),
    ]
    mech = models.ForeignKey(
        BattleMech, on_delete=models.PROTECT, related_name="segments"
    )
    max_armor = models.IntegerField(null=True, blank=True)
    current_armor = models.IntegerField(null=True, blank=True)
    max_internal_structure = models.IntegerField(null=True, blank=True)
    current_internal_structure = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name or str(self.id)

    def build_segment(self, segment_profile):
        self.name = segment_profile.get("name", "")
        self.max_armor = segment_profile.get("max_armor", 0)
        self.current_armor = self.max_armor
        self.max_internal_structure = segment_profile.get("max_internal_structure", 0)
        self.current_internal_structure = self.max_internal_structure
        self.build_components(segment_profile.get("components", ""))
        self.save()

    def build_components(self, components_profile):
        for component in components_profile:
            if components_profile[component].get("damage", ""):
                new_component = Weapon.objects.create(segment=self)
                new_component.build_weapon(components_profile[component])
            else:
                new_component = Component.objects.create(segment=self)
                new_component.build_component(components_profile[component])

    def repair_cost(self):
        armor_damage = self.max_armor - self.current_armor
        structure_damage = self.max_internal_structure - self.current_internal_structure
        return (
            (REPAIR_COST * armor_damage)
            + (REPAIR_COST * structure_damage)
            + self.component_repair_cost()
        )

    def component_repair_cost(self):
        components = Weapon.objects.filter(segment=self)
        repair_cost = 0
        for component in components:
            repair_cost += component.repair_cost()
        return repair_cost

    def destroy(self):
        self.current_armor = 0
        self.current_internal_structure = 0
        self.save()

    def is_destroyed(self):
        if self.current_internal_structure == 0:
            return True


class Component(Equipment):
    max_hit_points = models.IntegerField(default=1)
    current_hit_points = models.IntegerField(default=1)
    disabled = models.BooleanField(default=False)
    segment = models.ForeignKey(
        Segment, on_delete=models.PROTECT, related_name="components"
    )
    special_rule = models.TextField(max_length=500, blank=True)

    def build_component(self, component_profile):
        self.build_equipment(component_profile)
        self.save()

    def disable(self):
        if self.disabled:
            self.disabled = False
        else:
            self.disabled = True

    def is_disabled(self):
        return self.disabled

    def destroy(self):
        self.current_hit_points = 0

    def is_destroyed(self):
        if self.current_hit_points == 0:
            return True

    def repair_cost(self):
        cost_per_hit_point = self.value / self.max_hit_points
        return (
            cost_per_hit_point * (self.max_hit_points - self.current_hit_points)
        ) * REPAIR_COST


class Weapon(Component):
    damage = models.IntegerField(null=True, blank=True)
    heat = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=30, null=True, blank=True)
    min_range = models.IntegerField(null=True, blank=True)
    short_range = models.IntegerField(null=True, blank=True)
    med_range = models.IntegerField(null=True, blank=True)
    long_range = models.IntegerField(null=True, blank=True)

    def build_weapon(self, weapon_profile):
        self.damage = weapon_profile.get("damage", 0)
        self.heat = weapon_profile.get("heat", 0)
        self.min_range = weapon_profile.get("min_range", 0)
        self.short_range = weapon_profile.get("short_range", 0)
        self.med_range = weapon_profile.get("med_range", 0)
        self.long_range = weapon_profile.get("long_range", 0)
        self.build_component(weapon_profile)
        self.save()
