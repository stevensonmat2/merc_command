from . import views
from django.urls import path

urlpatterns = [
    path("create_mech/", views.create_mech, name="create_mech"),
    path("upload_mechs/<int:pk>/", views.upload_flechs_json_file, name="upload_mechs"),
    path("company_list/", views.company_list, name="company_list"),
]
