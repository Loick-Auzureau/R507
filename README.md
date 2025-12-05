## Docker

Si vous voulez containeriser l'application, voici des commandes utiles (PowerShell) :

Construire l'image depuis la racine du projet :
```pwsh
docker build -t r507-app .
```

Lancer le conteneur et mapper le port 8000 :
```pwsh
docker run --rm -p 8000:8000 r507-app
```
