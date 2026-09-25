#!/bin/bash

if [ -z "${ARG}" ]; then
  ARG="$1"
fi

echo "Updating $ARG"
curl -g "$CKAN_SOLR_URL/update?commit=true" \
     -H 'Content-Type: application/json' \
     -d '{"delete":{"query":"site_id:dgu_organisations_2 AND name:'$ARG'"}}'

ckan datagovuk reindex-organisations