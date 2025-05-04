#!/bin/bash

PROJECT_HOME="/workspaces/fastapi/"
# Example of a request to create a new user
curl -X 'POST' \
  'http://127.0.0.1:8000/user' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d "@${PROJECT_HOME}test/sample_data/user.json"

PROJECT_HOME="/workspaces/fastapi/"
# Example of a request to create a new company
curl -X 'POST' \
  'http://127.0.0.1:8000/company' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d "@${PROJECT_HOME}test/sample_data/company.json"

PROJECT_HOME="/workspaces/fastapi/"
# Example of a request to create a new team
curl -X 'POST' \
  'http://127.0.0.1:8000/team' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d "@${PROJECT_HOME}test/sample_data/team.json"

PROJECT_HOME="/workspaces/fastapi/"
# Example of a request to create a new resource
curl -X 'POST' \
  'http://127.0.0.1:8000/resource' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d "@${PROJECT_HOME}test/sample_data/resource.json"
