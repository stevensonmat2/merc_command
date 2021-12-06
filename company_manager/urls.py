from . import views
from django.urls import path

urlpatterns = [
    path('create_mech/', views.create_mech, name='create_mech'),
]
