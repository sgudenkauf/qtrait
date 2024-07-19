from django.shortcuts import render, redirect
from django.contrib.staticfiles import finders
import json
import plotly.graph_objs as go
from plotly.offline import plot
from . import models
from . import forms
from .models import Genre, Service
from .forms import UploadFileForm


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


def feature_new(request):
    if request.method == "POST":
        form = forms.CreateFeature(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = forms.CreateFeature()
    return render(request, "navigator/feature_new.html", {"form": form})


def show_genres(request):
    return render(request, "navigator/genres.html", {"genres": Genre.objects.all()})


def upload_file_view(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.cleaned_data["project"]
            service_name = form.cleaned_data["service_name"]
            file = request.FILES["file"]
            # Hier könnten Sie die Datei verarbeiten und in die Datenbank einfügen
            # Zum Beispiel:
            Service.objects.create(
                project=project,
                name=service_name,
                description="Uploaded File",
                serviceID="ServiceID",
            )
            return redirect("success_url")  # Leiten Sie zu einer Bestätigungsseite um
    else:
        form = UploadFileForm()
    return render(request, "navigator/upload_file.html", {"form": form})
