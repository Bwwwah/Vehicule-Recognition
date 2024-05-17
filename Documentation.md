# Documentation Technique

Ce projet est dockerisé et ce présente sous la forme de plusieurs dossiers contenant chacun a minima un script en JS qui a une utilisation précise et un fichier dockerfile.

## Dépendances

Ce projet utilise la dernière version de node ainsi que des dépendances telle que crypto, node-fetch et fs.

## Downloader

Vous trouver içi un script JS qui contient la fonction `downloadImages` permet de télécharger les photos de la caméra distante grâçe au lien. Les photos sont hasher afin de les comparer et de s'assurer qu'il n'y ai pas de redondance. Elles sont nommés grâce à la date et l'heure précise dans la fonction `getFormattedTimestamp`. Vous pouvez augmenter le nombre de photos à prendre en modifiant la variable `nb_photos`. 

## Dataset

Le script permet de télécharger les images labellisés. La constante `imagesAndAnnotations`simplifie le fichier export.js. La majeur partie du code sert à prélever le lien et télécharger chaque photo grâce au fichier export.js