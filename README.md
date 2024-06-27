# Vehicule-Recognition

## Bienvenue sur le projet vehicule recognition !

Ce projet permet d'entrainer un réseau de neurones à reconnaîtres des véhicules, piétons etc.. sur la route.

Pour commencer téléchargez ce repo git en local. Assurez vous d'avoir docker d'installé sur votre ordinateur et c'est partie !

Voici un schéma de l'architecture du projet pour vous donner une idée du fonctionnement global :

![alt text](<Schema IA.png>)

## Downloader

Ce container permettra de récupérer les images sur la caméra cible toute les minutes. Si vous avez déja vos images passez au prochain chapitre.

Placez vous dans la racine du projet et ouvrez un terminal.
Tous d'abord construisez l'image :

```
docker build -t downloader ./Downloader
```

A présent lancez le conteneur comme ceci sous Windows :

```
docker run --rm -v .\Downloader\Data:/Data --name Downloader downloader
```

Sous Unix :

```
docker run --rm -v ./Downloader/Data:/Data --name Downloader downloader
```

Vous retrouverez vos photos dans Downloader -> Data

## Deploy

Pour lancer le projet assurez vous d'avoir bien lancé le docker Downloader puis faites :

docker build -t deploy -f ./Deploy/dockerfile .

docker run -v ./Downloader/Data:/app/Downloader/Data -p 8050:8050 --rm --name Deploy deploy

Maitenant sur http://127.0.0.1:8050 vous aurez votre Dashboard

## Partie Test 

### Label studio (Pour tests)

Ensuite rendez vous sur le site label studio. Créez un projet puis importez et enfin labelisez vos photos. Une fois ceci fait exportez vos données de labélisation au format JSON et renommez ce fichier "export.json". Placez le à la racine du projet.

### Dataset (Pour tests)

Ce container va télécharger vos photos labelisés.

Placez vous à nouveau à la racine du projet et entrez cette commande :

```
docker build -t dataset -f ./Dataset/dockerfile .
```

A présent lancez votre container comme ceci sous windows :

```
docker run --rm -v .\Dataset\Images:/Images -v .\Dataset\labels:\labels --name Dataset dataset
```

Sous Unix :

```
docker run --rm -v ./Dataset/Images:/Images -v ./Dataset/labels:/labels --name Dataset dataset
```

Attendez la fin du téléchargement.
Vos photos seront enregistrés sous : Dataset -> Images.
labels.json contient une version simplifé de votre export.json.
