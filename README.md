# qtrait
An app to model the features and quality characteristics of software/system architectures.

## Database setup

```
python manage.py makemigrations
python .\manage.py migrate
```

## Run app (dev-mode)

Run app on local machine:
```
python manage.py runserver
```

Open feature form:
```
http://127.0.0.1:8000/feature-new/
```
## Admin
```
username: jade
pw: qtraid
```
## requirements.txt


Eine requirements.txt enthält die notwendigen Pakete für ein Python-Projekt mit der spezifischen Version. Mit pip install -r requirements.txt können die Pakete auf dem Zielsystem bereitgestellt werden. Für die Erstellung kann pip freeze > requirements.txt verwendet werden, das die Ausgabe der Konsole umleitet, die die Datei erstellt. 

```
pip install -r requirements.txt 
pip freeze > requirements.txt
```
