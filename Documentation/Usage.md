# 1) Usage:

---

## 1.Run:
After downloading the mEx models, place them as following: 

* _named_entity_recognition_mex_model.pt_ & _part_of_speech_tagger_mex_model.pt_ --> [SequenceTagger](https://github.com/DFKI-NLP/mEx-Docker-Deployment/tree/master/SequenceTagger)
* _relation_extraction_mex_model.pt_ --> [RelationExtraction](https://github.com/DFKI-NLP/mEx-Docker-Deployment/tree/master/RelationExtraction)

and proceed with the container deployment.

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

After making sure that all the docker services and API-endpoints are up and running, you could use the [**example.py**](https://github.com/DFKI-NLP/mEx-Docker-Deployment/blob/master/example.py) script to send and receive requests/responses.

The example script doesn't need any external libraries and could be used via python3

```shell
python example.py
```

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