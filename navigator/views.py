from django.shortcuts import render, redirect
from django.contrib.staticfiles import finders
from django.http import HttpResponse, JsonResponse
import json
from .models import Service, Feature, Project
from .forms import XMLUploadForm
from .xml_parser import parse_and_save_xml
import plotly.graph_objs as go
from plotly.offline import plot


def build_feature_dict(feature, processed_ids=None):
    """
    Baut eine hierarchische Datenstruktur
    """
    if processed_ids is None:
        processed_ids = set()

    # Überspringe bereits verarbeitete Features
    if feature.id in processed_ids:
        return None
    processed_ids.add(feature.id)

    children = feature.get_children()
    return {
        "id": feature.id,
        "name": feature.name,
        "children": [
            build_feature_dict(child, processed_ids)
            for child in children
            if child.id not in processed_ids
        ],
    }


def process_data_2(service, features):
    labels = []
    parents = []
    ids = []
    processed_ids = set()  # Verarbeitete IDs speichern

    def add_feature_to_sunburst(feature, parent_id=None):
        current_label = feature["name"]
        current_id = (parent_id + "|" + current_label) if parent_id else current_label

        # Überspringe bereits verarbeitete Features
        if current_id in processed_ids:
            return
        processed_ids.add(current_id)

        labels.append(current_label)
        ids.append(current_id)
        parents.append(parent_id if parent_id else "")

        if "children" in feature and feature["children"]:
            for child in feature["children"]:
                add_feature_to_sunburst(child, current_id)

    # Der Service ist die Wurzel
    service_id = f"service_{service.id}"
    labels.append(service.name)
    ids.append(service_id)
    parents.append("")  # Service hat keinen Parent

    # Füge alle Features als Kinder hinzu
    for feature in features:
        add_feature_to_sunburst(feature, service_id)

    return labels, parents, ids


def starting_page(request):

    # Lädt ein statisches JSON-File

    json_file_path = finders.find("navigator/data.json")
    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)

    labels, parents, ids = process_data_2([json_data])

    fig = go.Figure(go.Sunburst(labels=labels, parents=parents, ids=ids))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    # Diagramm als div ausgeben. include_plotlyjs=False, da wir plotly im Template laden.
    diagram_div = plot(fig, output_type="div", include_plotlyjs=False)

    return render(request, "navigator/sunburst.html", {"diagram_div": diagram_div})


def upload_xml(request):

    #  Hochladen einer XML-Datei und das Importieren der Daten in die Datenbank

    if request.method == "POST":
        form = XMLUploadForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES["xml_file"]

            existing_project = form.cleaned_data.get("existing_project")
            new_project_name = form.cleaned_data.get("new_project_name")
            new_project_owner = form.cleaned_data.get("new_project_owner")
            new_project_description = form.cleaned_data.get("new_project_description")

            if existing_project:
                project = existing_project
            else:
                project = Project.objects.create(
                    name=new_project_name,
                    owner=new_project_owner,
                    description=new_project_description,
                )

            # Verarbeite die XML-Datei und speichere Daten in der DB
            parse_and_save_xml(xml_file, project)
            return HttpResponse("XML erfolgreich eingelesen!")
    else:
        form = XMLUploadForm()

    return render(request, "navigator/upload.html", {"form": form})


def project_service_selection(request):

    # Auswahl eines Projekts und eines Services

    projects = Project.objects.all()
    return render(request, "navigator/project.html", {"projects": projects})


def get_services(request, project_id):

    # Gibt alle Services eines Projekts als JSON zurück.

    services = Service.objects.filter(project_id=project_id)
    services_data = [{"id": service.id, "name": service.name} for service in services]
    return JsonResponse(services_data, safe=False)


def get_sunburst_data(request, service_id):

    # Gibt die Sunburst-Daten für einen Service zurück.

    service = Service.objects.get(id=service_id)

    # Nur Wurzelknoten verarbeiten
    root_features = service.feature_set.filter(parent__isnull=True)
    data = [build_feature_dict(feature) for feature in root_features]

    labels, parents, ids = process_data_2(service, data)

    return JsonResponse({"labels": labels, "parents": parents, "ids": ids}, safe=False)


def debug_sunburst_data(request, service_id):

    # Debug-View, um die rohen Daten, Labels und Parents zu inspizieren.

    service = Service.objects.get(id=service_id)
    features = service.feature_set.all()

    data = [build_feature_dict(feature) for feature in features]
    labels, parents, ids = process_data_2(data)

    return JsonResponse(
        {"raw_data": data, "labels": labels, "parents": parents, "ids": ids}, safe=False
    )
