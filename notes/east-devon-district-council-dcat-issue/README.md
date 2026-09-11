https://cddodatamarketplace.atlassian.net/jira/software/c/projects/DGUK/boards/727?assignee=5be04e16a86b3349680e5d83&selectedIssue=DGUK-881

## Notes

https://govuk.zendesk.com/agent/tickets/6772403

- The harvest endpoint looks like it is working well on a browser
  https://files.eastdevon.gov.uk/transparency/metadata/eddctransparencydatasets.json

- however on attempting to run a harvest locally with the docker stack it is failing
  - setting a breakpoint on `/usr/lib/ckan/venv/lib/python3.11/site-packages/ckanext/dcat/harvesters/base.py:99` indicates that the content loaded does not look correct as it is being loaded as bytes.
  - DCat extension has been upgraded to 2.4.4 but that didn't make any difference in the data that is from the request
  - try to get the content from the harveest using a CURL comman to see what happens
    - same binary file response on the CKAN docker container, but browsers are rendering the json correctly
    - on the Mac OS terminal the response is in json
  - use https://filesig.search.org/ to try to find out what file encoding is being used
    \xff\xfe{\x00\r\x00\n\x00"
  - trying on the CKAN integration pod and it is timing out
  