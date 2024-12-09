from django.urls import path

from . import views

app_name = "navigator"

urlpatterns = [
    path("", views.starting_page, name="starting-page"),
    path("upload-xml/", views.upload_xml, name="upload_xml"),
    path(
        "navigator/", views.project_service_selection, name="project_service_selection"
    ),
    path(
        "navigator/get-services/<int:project_id>/",
        views.get_services,
        name="get_services",
    ),
    path(
        "navigator/get-sunburst-data/<int:service_id>/",
        views.get_sunburst_data,
        name="get_sunburst_data",
    ),
    path(
        "navigator/debug-sunburst-data/<int:service_id>/",
        views.debug_sunburst_data,
        name="debug_sunburst_data",
    ),
]
