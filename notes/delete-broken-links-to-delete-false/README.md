## Summary

### Step 1 summary (delete resources by http-status)

17 September 2026

> For integration, a total of *14,752 out of 15,343* resources were deleted

18 September 2026

> For staging, a total of *14,756 out of 15,343* resources were deleted

> For production, a total of *14,743 out of 15,343* resources were deleted

### Step 2 summary (delete resources by domain)

18 September 2026

> For integration A total of *5888 out of 13796* resources were deleted


# Notes

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

`retry.py` was renamed and updated to now be `filter_resources.py` , which no longer does a check on the URL as we have recently used playwright to retry those links.

## Step 1 Deleting resoruces by status

This `notes/delete-broken-links-to-delete-false/step1_filter_resources_result.csv` is the output after running `filter_resources.py` with these filters:

- Filter by to-delete=false
- Filter out http-status=200s
- Filter out deferred orgs
- Filter by http-status / http-category of: 404,410,TIMEOUT,CONNECTION_ERROR,SERVER_ERROR,DNS_ERROR

### Dry-run in Integration

We ran a dry-run deletion process for `notes/delete-broken-links-to-delete-false/step1_filter_resources_result.csv` and it was *going to* delete `14756 out of 15343 total resources` in Integration.

587 resources were skipped. We did a sample check of 4 and found that the state was already set to deleted for them.

The immediate plan is to update the process.py deletion script to output a csv of all the resources that were not able to be deleted. This means we can later investigate way and unblock the deletion process for 14756 resources.

---

16 September 2026

We plan on going ahead with deleting 14756 in integration

---

### Deployment to integration

17 September 2026

> A total of *14,752 out of 15,343* resources were deleted in Integration

#### Running the deletion script

We ran the [deletion script via govuk-dgu-charts](https://github.com/alphagov/govuk-dgu-charts/pull/1275/changes) and provided the input `notes/delete-broken-links-to-delete-false/step1_filter_resources_result.csv` ([govuk-dgu-charts PR](https://github.com/alphagov/govuk-dgu-charts/pull/1275/changes)). This included the flags `-set-state deleted` `--mode live`

The deletion script results were:

```bash
2026-09-17 13:48:23,839 - INFO - deleted 14752 resources, 3779 packages to reindex
```

The output CSV was `notes/delete-broken-links-to-delete-false/integration/success/step1_successfully_deleted_resources_20260917T134748.csv`

The 591 resources that weren't deleted were outputted as a CSV here `notes/delete-broken-links-to-delete-false/integration/issues/step1_failed_to_delete_resources_output.csv`

---

> The day prior, when running the dry-run, we had 14,756 to delete. However, there were 4 duplicates on resource-id, they each have a different guid which we don't take into consideration in the deletion process so it gets skipped and added into the 591 skipped resources `step1_failed_to_delete_resources_output.csv`:

  - 1f0a15ff-6a63-441e-b385-60afb16faf91
  - 3b1a56a5-a568-4466-82ab-310ec3281ab3
  - 88356c3d-562f-467c-a0c1-5b05e571c6e3
  - 490fe701-0e7b-4030-a4b0-9ede8c0d85cf

The reindex was successful with:

```bash
2026-09-17 14:52:11,462 - INFO - CKAN reindex 3779/3779 - fff67f58-d6ca-407d-a3ca-7bfc00f32ec8 succeeded
```

#### Tech debt / Follow up work

*TODO:*

- [ ] Investigate why these 591 resources were not deleted. For instance, some may have resources with state deleted or lacking package ids or different guids

---

### Deployment to Staging

18 September 2026

> A total of *14,756 out of 15,343* resources were deleted in Staging

We ran the [deletion script via govuk-dgu-charts](https://github.com/alphagov/govuk-dgu-charts/pull/1275/changes) and provided the input `notes/delete-broken-links-to-delete-false/step1_filter_resources_result.csv` ([govuk-dgu-charts PR](https://github.com/alphagov/govuk-dgu-charts/pull/1275/changes)). This included the flags `-set-state deleted` `--mode live`

The deletion script results were:

```bash
2026-09-18 10:03:33,138 - INFO - deleted 14756 resources, 3779 packages to reindex
```

The output file of those successfully deleted are here `notes/delete-broken-links-to-delete-false/staging/staging_step1_successfully_deleted_resources_20260918T100234.csv`

```bash
2026-09-18 10:03:33,137 - INFO - report of resources not deleted: /script/output.file (587 skipped)
```

#### Tech debt / Follow up work

*TODO:*

- [ ] Investigate why these 587 resources were not deleted. For instance, some may have resources with state deleted or lacking package ids or different guids

### Deployment to Proudction

18 September 2026

> A total of *14,743 out of 15,343* resources were deleted in Production

We ran the [deletion script via govuk-dgu-charts](https://github.com/alphagov/govuk-dgu-charts/pull/1275/changes) and provided the input `notes/delete-broken-links-to-delete-false/step1_filter_resources_result.csv` ([govuk-dgu-charts PR](https://github.com/alphagov/govuk-dgu-charts/pull/1275/changes)). This included the flags `-set-state deleted` `--mode live`

The deletion script results were:

```bash
2026-09-18 10:09:45,635 - INFO - deleted 14743 resources, 3779 packages to reindex
```

The output file of those successfully deleted are here `notes/delete-broken-links-to-delete-false/production/production_step1_successfully_deleted_resources_20260918T100234.csv`

```bash
2026-09-18 10:09:45,634 - INFO - report of resources not deleted: /script/output.file (600 skipped)
```

#### Tech debt / Follow up work

*TODO:*

- [ ] Investigate why these 600 resources were not deleted. For instance, some may have resources with state deleted or lacking package ids or different guids

## Step 2 Deleting resoruces by domain

This `notes/delete-broken-links-to-delete-false/step2_filtered_resources_by_invalid_domains.csv` is the output after running `filter_resources.py` with these filters:

Filter by to-delete=false
Filter out http-status=200s
Filter out deferred orgs (`notes/delete-broken-links-to-delete-false/orgs-to-defer.txt`)
Filter by invalid domains (`notes/delete-broken-links-to-delete-false/domains-to-delete.txt`)

### Deployment to integration

18 September 2026

> A total of *5888 out of 13796* resources were deleted in Integration

#### Running the deletion script

We ran the [deletion script via govuk-dgu-charts](https://github.com/alphagov/govuk-dgu-charts/pull/1285) and provided the input `notes/delete-broken-links-to-delete-false/step2_filtered_resources_by_invalid_domains.csv` ([govuk-dgu-charts PR](https://github.com/alphagov/govuk-dgu-charts/pull/1285/changes)). This included the flags `-set-state deleted` `--mode live`

The deletion script results were:

```bash
2026-09-18 13:49:51,534 - INFO - deleted 5888 resources, 3754 packages to reindex
```

The output file of those successfully deleted are here `notes/delete-broken-links-to-delete-false/step_2/integration/success/integration_step2_deleted_20260918T132630.csv`

```bash
2026-09-18 13:49:51,533 - INFO - report of resources not deleted: /script/output.file (7908 skipped)
```

#### Tech debt / Follow up work

*TODO:*

- [ ] Investigate why these 7908 resources were not deleted. Assumption is that they were deleted as part of Step 1 - delete resource by http status

### Deployment to Staging

### Deployment to Production