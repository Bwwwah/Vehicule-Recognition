# Vehicule-Recognition

docker build -t downloader ./Downloader
docker run -d --rm -v ./Downloader/Data:/Data --name Downloader downloader

docker build -t dataset -f ./Dataset/dockerfile .
docker run -d --rm -v ./Dataset/Images:/Images --name Dataset dataset