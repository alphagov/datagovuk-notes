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

---

We ran a dry-run deletion process for `notes/delete-broken-links-to-delete-false/step1_filter_resources_result.csv` and it was *going to* delete 14756 out of 15343 total resources in integration.

587 resources were skipped. We did a sample check of 4 and found that the state was already set to deleted for them.

The immediate plan is to update the process.py deletion script to output a csv of all the resources that were not able to be deleted. This means we can later investigate way and unblock the deletion process for 14756 resources.

---

After outputting the csv `notes/delete-broken-links-to-delete-false/issues/step1_filter_resources_result_not_deleted_20260917T081924.csv` and running an SQL statement to check how many had a state of "deleted"

329 of 587 resources have state as deleted

The other 258 of 587 resources don't exist in the table. They may have been hard deleted already.

---

We plan on going ahead with deleting 14756 in integration
