https://cddodatamarketplace.atlassian.net/issues?jql=textfields%20~%20%22solr*%22&wildcardFlag=true&selectedIssue=DGUK-1035

## Summary

The solr index rebuild process was breaking on Integration and Staging, which has meant that the solr index and the database are out of sync. 
This problem surfaced again when trying to investigate and fix the activity stream 500 errors for publishers. In order to get a full representation of the 500 error on EKS I had to get the solr reindex to complete after doing a database restore from an Integration database dump. 

2 datasets were identified as causing the solr reindex to fail due to the status field content being larger than 32k in characters. In order to get the rebuild to complete I had 2 options, either to trim the content down to under 32k or increase the size limit of the status field. I chose to trim it down as I realised upon inspection of the data that it would be possible to do this without impacting the publisher experience.

A full rebuild was successfully completed on my local docker stack.

### Main takeaways

* The harvest object_error_summary field which is used to inform publishers of data issues was causing the solr index rebuild outage. I decided to trim this down as there shouldn't be a need to show 32k characters worth of errors to the publisher, they will be able to see errors which were trimmed after fixing errors in their data.
* THe harvest job errors are already trimmed to show only 20 of the most frequent errors. I chose not to trim the error list down to 20 as there is still the possibility of the 32k character limit being exceeded if an error block is too large. 
* Now that we have more confidence of the solr reindex completing properly we can explore other solutions such as rebuilding the solr index with an alias and doing a switch over to limit downtime. This should eliminate any syncing issues between the solr index and the database.

## Notes

- During setup of CKAN restore for the investigation into 500 error responses from CKAN activity stream
    - error message returned from system
    ```
    Solr returned an error: Solr responded with an error (HTTP 400): [Reason: Exception writing document id d567ac8c55028d3374a13231338d577d to the index; possible analysis error: Document contains at least one immense term in field="status" (whose UTF8 encoding is longer than the max length 32766), all of which were skipped. ...
    ```
    - on docker stack -
        - updated the code on line 217 at /usr/lib/ckan/venv/src/ckan/ckan/lib/search/__init__.py to help identify the datasets that were failing
          - c9eeaa17-2291-4170-93ca-aec634aa0d63, 1a2a2e3d-a51e-4046-8c8b-e8ad3856dd9d
          - they are both harvest type datasets
          - the status field in the status field is far too long, so potentially not usable,
          - 1a2a2e3d-a51e-4046-8c8b-e8ad3856dd9d, belongs to CEFAS, it looks like theiir last harvest run was in April 2022
          - c9eeaa17-2291-4170-93ca-aec634aa0d63, belongs to SpattialData.gov.scot
          - the object_error_summary list could probably be trimmed down to allow correct reindexing of the dataset
        - alsoo set a breakpoint here /usr/lib/ckan/venv/src/ckan/ckan/lib/search/index.py(296) - just before solr connection to see what data was being pushed to solr
        - on the ckanext-datagovuk repo at line 76 on /usr/lib/ckan/venv/src/ckanext-datagovuk/ckanext/datagovuk/action/get.py, I checked whether the offending element was accessible and could be modified on our extension
          - after some testing this was proven to be true, the object_error_summary can be updated to limit the object error summary that was causing the solr reindex outage
          - PR created to trim down the object_error_summary until it is below the solr field limit
        - tested on the local docker stack, going to the CEFAS harvest jobs page showed that it only lists the 20 most frequest errors
          - so we could potentially just list the 20 most frequent errors, but there is the potential that some of these errors might be quite large
