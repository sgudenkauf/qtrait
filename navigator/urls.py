from django.urls import path

from . import views

app_name = "navigator"

urlpatterns = [
    path("", views.starting_page, name="starting-page"),
    path("feature-new/", views.feature_new, name="feature-new"),
]
