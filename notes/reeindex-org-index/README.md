https://cddodatamarketplace.atlassian.net/jira/software/projects/DGUK/boards/727?filter=assignee%20%3D%205be04e16a86b3349680e5d83&groupBy=custom&selectedIssue=DGUK-1023

## Summary

### Issue

ONS identified an incorrect contact email on their datasets, thay had updated their organisation contact information but this wasn't picked up on the dataset.

### Solution

The dataset will default to the contact information found in the organisations index if it isn't set in the dataset itself. 
So to get the organisation index updated we have to remove the publisher and run an organisation reindex.

## Notes

- check that the contact info is empty for a dataset in solr which is wrong as then it will default to the organisation index contact information

```
curl "$CKAN_SOLR_URL/query?rows=1600" -d '
{
  query : "*",
  filter: "name:gross_domestic_expenditure_on_research_and_development"
}'
```

- once no contact info is set, then confirm that the contact info matches the org index contact info 

```
curl -g "$CKAN_SOLR_URL/query" \
    -H 'Content-Type: application/json' \
    -d '{"query":"site_id:dgu_organisations_2 AND name:office-for-national-statistics"}'
```

- if this matches then we will have to delete the existing record in the org index before doing a rebuild to pick up the new contact info
  - there is a ticket in the backlog to pick up updates and deletions

```
curl -g "$CKAN_SOLR_URL/update?commit=true" \
     -H 'Content-Type: application/json' \
     -d '{"delete":{"query":"site_id:dgu_organisations_2 AND name:office-for-national-statistics"}}'
```

- now do a org index rebuild after a successful deletion from the index

```
ckan datagovuk reindex-organisations
```

- finally got something working on the EKS cluster, issue was to do with the shell script not picking up the arg passed to it, in the end the arg has to be set as an env var to pass it in
  - it is still possible to run the `reindex_org.sh` with an arg or with an env var
