from django.contrib import admin
from django.apps import apps
from .domain.models import User

admin.site.register(User)
models = apps.get_app_config("company_manager").get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
