# Data Ingestion Pipeline


## Description

This is a project created to be run in a Docker environment, in which we extract, ingest and also query the data that is on the server.

The "load_data.py" file is responsible for fetching data from the server and ingesting it into a postgres database that is running

The query_results.sql file is responsible for making the query reaching the final objective of the challenge.

By running the commands you will automatically run the scripts and you will only need to run one last command to be able to visualize the data as desired by the challenge


### Prerequisites

- Docker
- Docker Compose



## Instructions for Execution

1 - clone the repository https://github.com/PedroRodriguezx/challenge/ to your terminal

2 - execute the commands in this order to upload the containers, run the scripts and obtain the final query: 

docker-compose up -d

docker exec -it postgres_container psql -U myuser -d mydatabase -f /docker-entrypoint-initdb.d/query_report.sql


