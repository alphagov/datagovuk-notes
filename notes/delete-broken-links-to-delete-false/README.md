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

16 September 2026

We plan on going ahead with deleting 14756 in integration

---

17 September 2026

We ran the deletion script with input `notes/delete-broken-links-to-delete-false/step1_filter_resources_result.csv` (`https://github.com/alphagov/govuk-dgu-charts/pull/1275/changes`)

and flags `-set-state deleted` `--mode live`

The output CSV was `/script/data_deleted_20260917T134748.file`

The deletion script results were:

```bash
2026-09-17 13:48:23,839 - INFO - deleted 14752 resources, 3779 packages to reindex
```

A total of *14,752 out of 15,343.* resources were deleted

The reindex was successful with:

```bash
2026-09-17 14:52:11,462 - INFO - CKAN reindex 3779/3779 - fff67f58-d6ca-407d-a3ca-7bfc00f32ec8 succeeded
```

---

The 591 resources that weren't deleted were outputted as a CSV here

`notes/delete-broken-links-to-delete-false/issues/step1_failed_to_delete_resources_output.csv`

For example, there were 4 duplicates on resource-id, they each have a different guid which we don't take into consideration in the deletion process so it gets skipped and added into the 591 `step1_failed_to_delete_resources_output.csv`:

  - 1f0a15ff-6a63-441e-b385-60afb16faf91
  - 3b1a56a5-a568-4466-82ab-310ec3281ab3
  - 88356c3d-562f-467c-a0c1-5b05e571c6e3
  - 490fe701-0e7b-4030-a4b0-9ede8c0d85cf


*TODO:*

- [ ] Analyse these 591 resources: some may have resources with state deleted or lacking package ids etc.
