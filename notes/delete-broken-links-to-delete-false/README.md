## Notes

- Joes notes on broken links to-delete=false

https://beisgov.sharepoint.com/:w:/r/sites/OCDO/_layouts/15/Doc.aspx?sourcedoc=%7BBF293587-7B9D-46E2-8C24-3B31601DD99E%7D&file=2026%2009%20Broken%20links%20to%20delete%20false%20notes.docx&action=default&mobileredirect=true&wdOrigin=OUTLOOK-METAOS.FILEBROWSER

- notes from chat with Joe on 9th September 2026

```
to-delete=false
remove any deferred orgs
remove any 200s
then 2 passes:
1: filter to:

- 404
- 410
- Timeout
- Connection error
- Server error
- DNS error

(i.e filter out 403 and client_error)

2: filter to domains 
```

- orgs to deferred have been extracted from this spreadsheet 
    https://beisgov.sharepoint.com/:x:/r/sites/OCDO/_layouts/15/Doc.aspx?sourcedoc=%7BC40B0F67-3B79-4F80-BE3C-B2F430616509%7D&file=2026%2006%20Broken%20links%20responses.xlsx&action=default&mobileredirect=true
- `python retry.py -o orgs-to-defer.txt check_links_report.csv /tmp/output.csv`
  - the output from the run was that it removed the orgs in the org-to-defer.txt file and only put in the other org
  - testing the retry.py script with a `-d False` flag to run the script to filter by rather than filter out the orgs also ran with the expected results in the output.csv file
- we also need to filter by `404` and `410` in status, `TIMEOUT`, `CONNECTION_ERROR`, `SERVER_ERROR`, `DNS_ERROR`, as we have more confidence that these should be deleted as discussed with Joe on a call on.
  - we should generate a report on the numbers of what will be deleted as part of the log output
