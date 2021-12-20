import random
from django.db.models import Q
from company_manager.domain.models import Equipment, BaseModel


from django.db import models


class Character(BaseModel):
    pass


class PlotDevice(BaseModel):
    pass


class Plot(BaseModel):
    pass


class Setting(BaseModel):
    pass


class Conflict(BaseModel):
    pass


class Resolution(BaseModel):
    pass


class Mission(models.Model):
    setting = models.ForeignKey(
        Setting, on_delete=models.CASCADE, related_name="missions"
    )
    salvage_points = models.IntegerField()
    payment = models.DecimalField(max_digits=11, decimal_places=2)
    # origin_faction = models.ForeignKey()
    # contracted_faction = models.ForeignKey()
    # targeted_faction = models.ForeignKey()

    def create_mission(self, mission_profile):
        self.setting = self.get_mission_setting(mission_profile)
        self.set_mission_rewards(mission_profile)
        self.payment = mission_profile.get("payment", 0)
        self.origin_faction = mission_profile.get("origin_faction", "")
        self.contracted_faction = m

    def get_mission_setting(self, mission_profile):
        setting_choice = random.choice(mission_profile.get("potential_settings", []))
        try:
            setting = Setting.objects.get(name=setting_choice)
            return setting
        except Setting.DoesNotExist:
            return None

    def set_mission_rewards(self, mission_profile):
        reward_count = mission_profile.get("reward_count", 0)
        potential_rewards = list(
            Reward.objects.filter(
                Q(value <= self.contracted_faction.reward_range())
                & Q(production_year <= self.contracted_faction.current_year())
            )
        )
        rewards = random.choices(potential_rewards, k=reward_count)

        for reward in rewards:
            new_reward = Reward.objects.create()
            new_reward.clone(reward)
            new_reward.mission = self


class Reward(Equipment):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    pass


class Campaign(BaseModel):
    pass
