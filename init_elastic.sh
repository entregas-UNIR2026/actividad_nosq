#!/bin/bash
curl -X PUT "http://localhost:9200/articulos" -H 'Content-Type: application/json' -d'{"settings": {"number_of_shards": 1, "number_of_replicas": 0}}'
curl -X POST "http://localhost:9200/articulos/_doc/1" -H 'Content-Type: application/json' -d'{"nombre": "Monitor", "precio": 150}'
