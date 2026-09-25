https://cddodatamarketplace.atlassian.net/jira/software/projects/DGUK/boards/727?filter=textfields%20~%20%22environment%20agency*%22&groupBy=custom&selectedIssue=DGUK-944

## Summary

The Environment Agency Data Sharing Platform harvest source started creating duplicate datasets on 6th August 2026, it's not entirely clear why they were generated and initially the publisher wanted to remove the more recent duplicates. After a bit more thinking they changed their minds and now want to delete the original datasets keeping the newer ones. 

### Solution

The script was copied over from the scripts repo into this repo to keep work on CKAN tickets in this repo to make it easier to find solutions for similar issues. It was tested on Integration before being deployed to Staging and Production.

Logs available - `ea-remove-duplicates.log`

## Notes

- Environment Agency finally came back with a decision to keep the latest datasets and remove the older one as duplicates
- The script `delete_duplicate_datasets_by_org.py` was copied from `datagovuk-scripts` repo - https://raw.githubusercontent.com/alphagov/datagovuk-scripts/7e0dbe9ff0edc9e6963d7d694e2914dc9981f149/remove-datasets/remove_datasets.py, as this was used in the original PR before `datagovuk-notes` repo was created
- the args to pass to the script will be
  - `--org environment-agency --log-dir /script --solr-only False --remove-all False --report-only True --keep-latest True`
