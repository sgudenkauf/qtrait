from django.shortcuts import render
from django.contrib.staticfiles import finders
import json
import plotly.graph_objs as go
from plotly.offline import plot
from . import models
from . import forms


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
