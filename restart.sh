#!/usr/bin/env bash

docker-compose --env-file=config.env down
docker volume rm elasticsearch-pubmed 
docker volume rm pubmed-elasticsearch_elasticsearch-pubmed
docker volume create elasticsearch-pubmed 
docker volume create pubmed-elasticsearch_elasticsearch-pubmed
docker-compose --env-file=config.env up -d --build
