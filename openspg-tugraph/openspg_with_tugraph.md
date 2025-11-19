
# Get the docker-compose file
curl -sSL https://raw.githubusercontent.com/OpenSPG/openspg/master/dev/release/docker-compose.yml -o docker-compose.yml

# Start the server
docker-compose up -d

https://github.com/OpenSPG/openspg/blob/master/dev/release/docker-compose.yml

and defines the containers:
openspg-server, openspg-mysql, tugraph, and elasticsearch.


# Get the docker-compose file
curl -sSL https://raw.githubusercontent.com/OpenSPG/openspg/master/dev/release/docker-compose.yml -o docker-compose.yml

# Start the server
docker-compose up -d