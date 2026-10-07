https://cddodatamarketplace.atlassian.net/jira/software/projects/DGUK/boards/727?filter=assignee%20%3D%205be04e16a86b3349680e5d83&groupBy=custom&selectedIssue=DGUK-205

## Notes

- The activity stream was not enabled on the local dev stack so I got it working to see if it would work
  - Once set up it was on a high level view but clicking on the activity caused a 500 error
  - setting breakpoint at /usr/lib/ckan/venv/lib/python3.11/site-packages/jinja2/environment.py:490
  - issue found on CKAN repo - https://github.com/ckan/ckan/issues/9459
  - fix in PR is here - https://github.com/jmtdev0-open-source/ckan/blob/93f178ea3187210cfd1ae6869eb2404e1d68bf7f/ckanext/tracking/templates/package/snippets/resource_item.html
  - as we override resource_item.html we will have to fix it in our override
  - code changes were made to the ckanext-datagovuk repo
    - built as a separate docker image and then referenced from dev.Dockerfile as we need to work around zscaler when running the stack locally
  - identified some bugs in the code due to a lag behind CKAN, so updated the templates in line with what is expected for the latest 2.10 release version
  - tried it out on Integration but am receiving 500 errors when attempting to show the publisher activity stream, the dataset activity stream is working as expected
  - now trying to restore an Integration db on my machine so that I can investigate and debug issues properly
    - finally managed to restore the back up on my machine, to download it I had to go via the AWS console as admin because using the AWS CLI kept timing out due to session token refreshes
    - attempting to restore it in docker but it kept timing out as docker was able to use all of the disk space on my machine, so had to limit docker from using all the disk space and remove redundant images but this still wasn't enough to enable a restore in docker
    - switched to restoring on to local native postgres server and it completed in about 1.5 hours
    - next will test that CKAN can connect to the postgres server running on my machine
    - managed to reindex CKAN but there were 2 datasets which were causing the solr index rebuild to fail 
      - c9eeaa17-2291-4170-93ca-aec634aa0d63, 1a2a2e3d-a51e-4046-8c8b-e8ad3856dd9d
      - will investigate these datasets as there is probably a data problem causing the reindex to fail with a Solr status which is reported as a massive field of over 32k
      - error message returned from system
      ```
      Solr returned an error: Solr responded with an error (HTTP 400): [Reason: Exception writing document id d567ac8c55028d3374a13231338d577d to the index; possible analysis error: Document contains at least one immense term in field="status" (whose UTF8 encoding is longer than the max length 32766), all of which were skipped. ...
      ```
      - on docker stack -
        /usr/lib/ckan/venv/src/ckan/ckan/lib/search/index.py(174)
        /usr/lib/ckan/venv/src/ckan/ckan/lib/search/index.py(296) - just before solr connection

      - they are both harvest type datasets
      - the status field in the status field is far too long, so potentially not usable,
      - 1a2a2e3d-a51e-4046-8c8b-e8ad3856dd9d, belongs to CEFAS, it looks like theiir last harvest run was in April 2022
      - c9eeaa17-2291-4170-93ca-aec634aa0d63, belongs to SpattialData.gov.scot