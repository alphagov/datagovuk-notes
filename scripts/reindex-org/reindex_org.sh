#!/bin/bash

echo "Updating $1"
curl -g "$CKAN_SOLR_URL/update?commit=true" \
     -H 'Content-Type: application/json' \
     -d '{"delete":{"query":"site_id:dgu_organisations_2 AND name:'$1'"}}'

ckan datagovuk reindex-organisations