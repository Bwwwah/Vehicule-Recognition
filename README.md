# Vehicule-Recognition

## Bienvenue sur le projet vehicule recognition !

Ce projet permet d'entrainer un réseau de neurones à reconnaîtres des véhicules, piétons etc.. sur la route.

Pour commencer téléchargez ce repo git en local. Assurez vous d'avoir docker d'installé sur votre ordinateur et c'est partie !

## Downloader

Ce container permettra de récupérer les images sur la caméra cible toute les minutes. Si vous avez déja vos images passez au prochain chapitre.

Placez vous dans la racine du projet et ouvrez un terminal.
Tous d'abord construisez le container :

```
docker build -t downloader ./Downloader
```

A présent lancez le :

```
docker run -d --rm -v ./Downloader/Data:/Data --name Downloader downloader
```

Environ quatre-vingt dix photos devraient êtres prises sur une durée d'une heure et trente minutes. Une fois cela fini le container s'éteindra de lui même. Vous retrouverez vos photos dans Downloader -> Data

## Label studio

Ensuite rendez vous sur le site label studio. Créez un projet puis importez et enfin labelisez vos photos. Une fois ceci fait exportez vos données de labélisation au format JSON et renommez ce fichier "export.json". Placez le à la racine du projet.

## Dataset

Ce container va télécharger vos photos labelisés.

Placez vous à nouveau à la racine du projet et entrez cette commande :

```
docker build -t dataset -f ./Dataset/dockerfile .
```

A présent lancez votre container :

```
docker run -d --rm -v ./Dataset/Images:/Images --name Dataset dataset
```

Vos photos seront enregistrés sous : Dataset -> Images.
dataset.json contient une version simplifé de votre export.json.