from django.urls import path

from . import views

app_name = "navigator"

urlpatterns = [
    path("", views.starting_page, name="starting-page"),
    path("feature-new/", views.feature_new, name="feature-new"),
    path("genres/", views.show_genres, name="show-genres"),
    path("upload/", views.upload_file_view, name="upload_file"),
]
