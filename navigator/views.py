from django.shortcuts import render, redirect
from django.contrib.staticfiles import finders
from django.http import HttpResponse
import json
import plotly.graph_objs as go
from plotly.offline import plot
from . import models
from . import forms
from .models import Service, Feature, Project
from .forms import XMLUploadForm
from .xml_parser import parse_and_save_xml


def process_data(data, parent_name=""):
    labels = []
    parents = []
    for item in data:
        labels.append(item["name"])
        parents.append(parent_name)
        if "children" in item and item["children"]:
            child_labels, child_parents = process_data(item["children"], item["name"])
            labels.extend(child_labels)
            parents.extend(child_parents)
    return labels, parents


def starting_page(request):
    # Path to Data-File
    json_file_path = finders.find("navigator/data.json")

    # open JSON-Datei
    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)

    #
    labels, parents = process_data(json_data)

    # create Sunburst-Diagramm
    fig = go.Figure(
        go.Sunburst(
            labels=labels,
            parents=parents,
        )
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    # Sunburst to HTML-div
    diagram_div = plot(fig, output_type="div")

    return render(request, "navigator/sunburst.html", {"diagram_div": diagram_div})


def upload_xml(request):
    if request.method == "POST":
        form = XMLUploadForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES["xml_file"]

            # Existierendes Projekt
            existing_project = form.cleaned_data.get("existing_project")

            # Neues Projekt
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

            # Verarbeite die XML-Datei und speichere die Daten im ausgewählten/neuen Projekt
            parse_and_save_xml(xml_file, project)
            return HttpResponse("XML erfolgreich eingelesen!")
    else:
        form = XMLUploadForm()

    return render(request, "navigator/upload.html", {"form": form})
