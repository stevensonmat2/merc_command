from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("create_mech/", views.create_mech, name="create_mech"),
    path("upload_mechs/<int:pk>/", views.upload_flechs_json_file, name="upload_mechs"),
    path("company/<int:pk>/", views.company_view, name="company_view"),
    path("mech_detail/<uuid:pk>", views.mech_view, name="mech_view"),
]
