from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

REPAIR_COST = 10

ORIGIN_CHOICES = [
    ("CLAN", "Clan"),
    ("INNERSPHERE", "Inner-Sphere"),
]

FACTION_CHOICES = [()]


class Person(models.Model):
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


class MechWarrior(Person):
    piloting_skill = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(0)]
    )
    gunnery_skill = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(0)]
    )
    experience = models.IntegerField(default=0)
    max_health = models.IntegerField(default=5)
    current_health = models.IntegerField(default=5)


class Equipment(models.Model):
    name = models.CharField(max_length=30)
    variant = models.CharField(max_length=30)
    value = models.DecimalField(max_digits=11, decimal_places=2)
    weight = models.DecimalField(max_digits=8, decimal_places=2)
    origin = models.CharField(max_length=30, choices=ORIGIN_CHOICES)

    class Meta:
        abstract = True


class Component(Equipment):
    max_hit_points = models.IntegerField()
    current_hit_points = models.IntegerField()

    def destroy(self):
        self.current_hit_points = 0

    def is_destroyed(self):
        if self.current_hit_points == 0:
            return True

    def damage_cost(self):
        cost_per_hit_point = self.value / self.max_hit_points
        return (
            cost_per_hit_point * (self.max_hit_points - self.current_hit_points)
        ) * REPAIR_COST


class Weapon(Component):
    pass


class ComplexEquipment(Equipment):
    maintenance_upkeep = models.DecimalField(max_digits=11, decimal_places=2)


class DropShip(ComplexEquipment):
    mech_capacity = models.IntegerField()
    weight_limit = models.IntegerField()
    reliability = models.IntegerField()


class Segment(models.Model):
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
    name = models.CharField(choices=SEGMENT_NAME_CHOICES)
    mech = models.ForeignKey(BattleMech, on_delete=models.PROTECT)
    max_armor = models.IntegerField()
    current_armor = models.IntegerField()
    max_internal_structure = models.IntegerField()
    current_internal_structure = models.IntegerField()

    def repair_cost(self):
        armor_damage = self.max_armor - self.current_armor
        structure_damage = self.max_internal_structure - self.current_internal_structure
        return (
            (REPAIR_COST * armor_damage)
            + (REPAIR_COST * structure_damage)
            + self.component_damage_cost()
        )

    def component_damage_cost(self):
        components = Weapon.objects.filter(segment=self)
        component_damage_cost = 0
        for component in components:
            component_damage_cost += component.damage_cost()
        return component_damage_cost

    def destroy(self):
        self.current_armor = 0
        self.current_internal_structure = 0

    def is_destroyed(self):
        if self.current_internal_structure == 0:
            return True


class BattleMech(ComplexEquipment):
    head = models.ForeignKey(Segment, on_delete=models.CASCADE)
    center_torso = models.ForeignKey(Segment, on_delete=models.CASCADE)
    center_torso_rear = models.ForeignKey(Segment, on_delete=models.CASCADE)
    left_torso = models.ForeignKey(Segment, on_delete=models.CASCADE)
    left_torso_rear = models.ForeignKey(Segment, on_delete=models.CASCADE)
    right_torso = models.ForeignKey(Segment, on_delete=models.CASCADE)
    right_torso_rear = models.ForeignKey(Segment, on_delete=models.CASCADE)
    left_leg = models.ForeignKey(Segment, on_delete=models.CASCADE)
    right_leg = models.ForeignKey(Segment, on_delete=models.CASCADE)
    left_arm = models.ForeignKey(Segment, on_delete=models.CASCADE)
    right_arm = models.ForeignKey(Segment, on_delete=models.CASCADE)

    def total_repair_cost(self):
        repair_cost = 0
        segments = Segment.objects.filter(mech=self)
        for segment in segments:
            repair_cost += segment.repair_cost()
