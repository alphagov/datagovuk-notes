https://raw.githubusercontent.com/alphagov/datagovuk-scripts/7e0dbe9ff0edc9e6963d7d694e2914dc9981f149/remove-datasets/remove_datasets.py

## Notes

- Environment Agency finally came back with a decision to keep the latest datasets and remove the older one as duplicates
- The script `delete_duplicate_datasets_by_org.py` was copied from `datagovuk-scripts` repo - https://raw.githubusercontent.com/alphagov/datagovuk-scripts/7e0dbe9ff0edc9e6963d7d694e2914dc9981f149/remove-datasets/remove_datasets.py, as this was used in the original PR before `datagovuk-notes` repo was created
- the args to pass to the script will be
  - `--org environment-agency --log-dir /script --solr-only False --remove-all False --report-only True --keep-latest True`
