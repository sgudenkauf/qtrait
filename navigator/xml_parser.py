import xml.etree.ElementTree as ET
from .models import Service, Feature, Project


def parse_and_save_xml(xml_file, project):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Finden des Wurzelknoten
    struct = root.find("struct")
    service_node = struct.find("and")

    if service_node is None:
        raise ValueError("Kein Wurzel Knoten augefunden")

    # Name des Modells suchen als Service nutzren (Name des Modells)
    model_name = service_node.attrib.get("name")

    # Erstelle das Service-Objekt mit zugehǒrigen Modellnamen
    service = Service.objects.create(
        project=project,
        name=model_name,
        description=f"{model_name} Service",
        serviceID=model_name,
    )

    # Die Knoten Fetures verarbeiten
    for child in service_node:
        parse_features(child, service, None)


def parse_features(xml_node, service, parent):
    # Verarbeite  relevante Knoten
    if xml_node.tag not in ["feature", "and"]:
        return  # Überspringe Namenlosen Knoten (graphics)

    # Überprüfe auf "name" Attribut
    feature_name = xml_node.attrib.get("name")

    if feature_name is None:
        # ohne Name überspringen
        print(f"Knoten ohne Namen übersprungen: {xml_node.tag}")
        return

    # Beschreibung  aus dem XML extrahieren (Null moeglich)
    description = (
        xml_node.find("description").text
        if xml_node.find("description") is not None
        else ""
    )

    # Feature-Objekt erstellen
    feature = Feature.objects.create(
        service=service, name=feature_name, description=description, parent=parent
    )

    # Rekursive Verarbeitung Child-Knoten
    for child in xml_node:
        if child.tag == "and" or child.tag == "feature":
            parse_features(child, service, feature)
