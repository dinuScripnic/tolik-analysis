# Evaluation System

## Notes
1. You need C/C++ compiler to install a package(hdbscan) for clustering.
2. You need mongodb to store the data.
3. python3.10 because if not hdbscan will not work.
4. You need to install the requirements.txt file.
5. you need to install docker and docker image of mongodb.
```bash
sudo apt install docker.io
docker --version # to check if it is installed
sudo docker pull mongo
sudo docker run -d -p 27017:27017 --name mongodb mongo
# not mongodb is running on port 27017
docker start mongodb
```