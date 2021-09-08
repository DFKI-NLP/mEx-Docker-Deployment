# 1) Usage:

## 1.Run:

The first time docker compose is used it will need roughly 20~30 minutes depending on the performance of the given device 
and Network speed. The first run includes downloading the mEx models from the DFKI cloud and also installing the needed libraries
which sums up to (7.5 GB) 

```shell

git clone https://github.com/DFKI-NLP/mEx-Docker-Deployment.git
cd mEx-Docker-Deployment

# Start containers & run services
docker-compose up -d

# Stop containers & remove services
docker-compose down

```

Open browser to following address:

```shell

http://localhost:5000/

```


---


## Faster 1.Run:

There is also the possibility to download the models beforehand from the listed links in the mentioned [table](https://github.com/DFKI-NLP/mEx-Docker-Deployment#mex-models-overview).

The models need to be placed in the correct directories:

- [Part-of-Speech-Tagging](https://cloud.dfki.de/owncloud/index.php/s/e7G9deea7eRksCY/download) & [Named-Entity-Recognition](https://cloud.dfki.de/owncloud/index.php/s/WWbnqJ6N8gQQWMD/download) Models --> [SequenceTagger](https://github.com/DFKI-NLP/mEx-Docker-Deployment/tree/main/SequenceTagger)
- [Relation-Extraction](https://cloud.dfki.de/owncloud/index.php/s/cDHpdckyPx72gdY/download) Model --> [RelationExtraction](https://github.com/DFKI-NLP/mEx-Docker-Deployment/tree/main/RelationExtraction)

Following lines should be changed:

* [Dockerfile 1](https://github.com/DFKI-NLP/mEx-Docker-Deployment/blob/main/RelationExtraction/Dockerfile)
  - uncomment [line 10](https://github.com/DFKI-NLP/mEx-Docker-Deployment/blob/0ff83aca6b67e3cefc3c422d07e82666ee774189/RelationExtraction/Dockerfile#L10)
  - comment [line 11](https://github.com/DFKI-NLP/mEx-Docker-Deployment/blob/0ff83aca6b67e3cefc3c422d07e82666ee774189/RelationExtraction/Dockerfile#L11)

* [Dockerfile 2](https://github.com/DFKI-NLP/mEx-Docker-Deployment/blob/1f31e3263c19a7485bbc28b17d0dccc06cedeec2/SequenceTagger/Dockerfile)
  - uncomment [line 8](https://github.com/DFKI-NLP/mEx-Docker-Deployment/blob/0ff83aca6b67e3cefc3c422d07e82666ee774189/SequenceTagger/Dockerfile#L8)
  - uncomment [line 11](https://github.com/DFKI-NLP/mEx-Docker-Deployment/blob/0ff83aca6b67e3cefc3c422d07e82666ee774189/SequenceTagger/Dockerfile#L11)
  - comment [line 9](https://github.com/DFKI-NLP/mEx-Docker-Deployment/blob/0ff83aca6b67e3cefc3c422d07e82666ee774189/SequenceTagger/Dockerfile#L9)
  - comment [line 12](https://github.com/DFKI-NLP/mEx-Docker-Deployment/blob/0ff83aca6b67e3cefc3c422d07e82666ee774189/SequenceTagger/Dockerfile#L12)
  

---

## 2.Run in case of changes in the code

Depending on the changes the second run should be faster because Docker caches layers from previous runs 
and tries to utilize this to cut down on deployment time.

```shell
cd mEx-Docker-Deployment

# Start containers & run services & builds any changes
docker-compose up -d --build

# Stop containers & remove services
docker-compose down
```
---

## (Optional) Complete-Cleanup after runs:

```shell
# List all containers
docker ps -aq

# Stop all running containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -q)
```