from django.shortcuts import render, redirect
from django.contrib.staticfiles import finders
from django.http import HttpResponse, JsonResponse
import json
from .models import Service, Feature, Project
from .forms import XMLUploadForm
from .xml_parser import parse_and_save_xml
import plotly.graph_objs as go
from plotly.offline import plot


def build_feature_dict(feature):
    """
    Baut eine hierarchische Datenstruktur aus einem Feature-Objekt.
    Jede Node erhält "name" und eine Liste von "children".
    """
    children = feature.get_children()
    return {
        "name": feature.name,
        "children": [build_feature_dict(child) for child in children],
    }


def process_data_2(features):
    """
    Erzeugt aus einer Liste von hierarchischen Strukturen (features)
    Listen für Plotly Sunburst: labels, parents, ids.

    Ein künstlicher Root-Knoten namens "ROOT" wird angenommen.
    Wir generieren eindeutige IDs, um Ambiguitäten zu vermeiden.
    """
    labels = []
    parents = []
    ids = []

    def add_feature_to_sunburst(feature, parent_id=None):
        current_label = feature["name"]
        # Erzeuge eine eindeutige ID durch Kombination von parent_id und current_label
        current_id = (parent_id + "|" + current_label) if parent_id else current_label

        labels.append(current_label)
        ids.append(current_id)
        parents.append(parent_id if parent_id else "")

        if "children" in feature and feature["children"]:
            for child in feature["children"]:
                add_feature_to_sunburst(child, current_id)

    # Wir erwarten in features mindestens einen Root-Knoten.
    # Sollte der Nutzer bereits einen Root-Knoten nutzen, kannst du ihn direkt verwenden.
    # Hier fügen wir einen künstlichen ROOT-Knoten ein, falls nicht schon vorhanden.
    # Z.B. features sieht so aus: [{"name": "Architecture Overview", "children":[...]}]
    # Dann packen wir alles unter "ROOT".
    root = {"name": "ROOT", "children": features}

    add_feature_to_sunburst(root)

    return labels, parents, ids


def starting_page(request):
    """
    Lädt ein statisches JSON-File und zeigt ein Sunburst-Diagramm zur Demo an.
    """
    json_file_path = finders.find("navigator/data.json")
    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)

    # Wir erwarten hier, dass json_data bereits ein Wurzelobjekt darstellt.
    # Falls nicht, wie oben, künstlichen ROOT einführen.
    labels, parents, ids = process_data_2([json_data])

    fig = go.Figure(go.Sunburst(labels=labels, parents=parents, ids=ids))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    # Diagramm als div ausgeben. include_plotlyjs=False, da wir plotly im Template laden.
    diagram_div = plot(fig, output_type="div", include_plotlyjs=False)

    return render(request, "navigator/sunburst.html", {"diagram_div": diagram_div})


def upload_xml(request):
    """
    Ermöglicht das Hochladen einer XML-Datei und das Importieren der Daten in die Datenbank.
    """
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
    """
    Listet alle Projekte auf, aus denen ein Service ausgewählt werden kann.
    """
    projects = Project.objects.all()
    return render(request, "navigator/project.html", {"projects": projects})


def get_services(request, project_id):
    """
    Gibt alle Services eines Projekts als JSON zurück.
    """
    services = Service.objects.filter(project_id=project_id)
    services_data = [{"id": service.id, "name": service.name} for service in services]
    return JsonResponse(services_data, safe=False)


def get_sunburst_data(request, service_id):
    """
    Gibt die Daten für das Sunburst-Diagramm als JSON zurück,
    damit das Diagramm im Browser mit Plotly gerendert werden kann.
    """
    service = Service.objects.get(id=service_id)
    features = service.feature_set.all()

    # Hierarchische Datenstruktur aus den Features aufbauen
    data = [build_feature_dict(feature) for feature in features]

    labels, parents, ids = process_data_2(data)

    # Gebe die Daten für das Sunburst als JSON zurück
    return JsonResponse({"labels": labels, "parents": parents, "ids": ids}, safe=False)


def debug_sunburst_data(request, service_id):
    """
    Debug-View, um die rohen Daten, Labels und Parents zu inspizieren.
    """
    service = Service.objects.get(id=service_id)
    features = service.feature_set.all()

    data = [build_feature_dict(feature) for feature in features]
    labels, parents, ids = process_data_2(data)

    return JsonResponse(
        {"raw_data": data, "labels": labels, "parents": parents, "ids": ids}, safe=False
    )
