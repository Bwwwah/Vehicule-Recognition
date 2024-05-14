# Vehicule-Recognition

docker build -t downloader ./Downloader
docker run -d --rm -v ./Downloader/Data:/Data downloader 

docker build -t dataset -f ./Dataset/dockerfile .
docker run -d --rm -v ./Dataset/Images:/Images dataset