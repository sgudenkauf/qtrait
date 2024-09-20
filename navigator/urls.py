from django.urls import path

from . import views

app_name = "navigator"

urlpatterns = [
    path("", views.starting_page, name="starting-page"),
    path("upload-xml/", views.upload_xml, name="upload_xml"),
]
