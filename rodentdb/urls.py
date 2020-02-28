from django.urls import path
from .views import get_rodent_template

urlpatterns = [
    path("get_rodent_template/", get_rodent_template, name="get_rodent_template"),
]
