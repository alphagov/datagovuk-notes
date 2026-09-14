https://cddodatamarketplace.atlassian.net/jira/software/c/projects/DGUK/boards/727?assignee=5be04e16a86b3349680e5d83&selectedIssue=DGUK-881

## Summary

### Issues

Discovered 2 issues with the harvest source

* It is not possible to connect from the EKS pods to the harvest source as it is reporting a timeout. This error is reported on the harvest jobs error logs and can be replicated on Integration by running a curl command on the pod to the harvest source URL.
  * This might be because they are blocking bot access or access from our EKS IP range.

Solution - asked the publisher to allow through requests from our EKS IP range.

  ```
  34.249.23.204
  46.137.63.103
  52.51.83.47
  ```

* When running the harvest job on my docker stack I encountered a utf-8 decoding issue. It seems that the response from the hravest source was actually utf-16 which the DCat extension is unable to handle.

Solution - asked the publisher to change their server to respond in `utf-8` encoding and not `utf-16`.

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
    - this website - https://filesig.search.org/ seems to indicate it is utf-32 
    - but Joe helped to determine that the encoding is utf-16, as it's not supported by the DCat extension I will report back to the publisher to ask that they change the encoding of their response to `utf-8`
    - this is supported by the table from this website https://unicode.org/faq/utf_bom.html#BOM

  - I tested changing the encoding to `utf-16` and was able to successfully harvest 9 records locally
  - this is a short script below for testing the response decode

  ```
import requests

resp = requests.get("https://files.eastdevon.gov.uk/transparency/metadata/eddctransparencydatasets.json")

try:
  print('Trying to decode as utf-8')
  decoded = resp.content.decode('utf-8')
except Exception as e:
  print(f'\tException: {e}\n')
  print('Trying to decide as utf-16')
  if (resp.content.decode('utf-16')):
    print('\tSuccess')
  ```

  - on the Integration server however it was timing out and not reporting an encoding error
    - it's possible that the IP address range for the EKS cluster has been blocked so provide the IP range to them, supplied by the GOV.UK platform engineering team
    - we might also need to update them to let publisher know about new IP ranges if/when we build a new harvest pipeline.
