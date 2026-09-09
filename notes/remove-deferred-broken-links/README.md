## Summary

### Expected result

The removal of all broken links for deferred orgs after they have been already retried. 45 resources which were failing are now working so have been removed from the deletion process as they have been marked as FALSE under the to-delete column.

### Testing coverage

Local testing was set up to check that the scripts behaved as expected and a full test has been carried out on Integration to only remove resources that have been marked for deletion still retaining resources that should no longer be deleted.

### Main takeaways

- the retry script didn't use the URL from the database which would have been the latest updated by the publisher. This caused some confusion at the start of the work.
- the scripts processing on govuk-dgu-charts repo can be extended to suit a number of scenarios.

## Notes

https://cddodatamarketplace.atlassian.net/browse/DGUK-964 part 2

- extracted broken link resources to delete from spreadsheet `2026 06 Broken links responses` as there was some PII in the doc.
- orgs confirmeed to delete broken link resources - 
    dartmoor-national-park-authority
    department-for-transport
    nhs-blood-and-transplant
    office-of-rail-and-road
    plymouth-city-council
- retry script was also brought in from the alphagov/datagovuk-scripts/check-links-analysis/scripts/retry.py and updated to allow for targets orgs
- the broken_links_to_delete file was copied over as according to the timestamp that was the latest file generated
- initially the CKAN in the docker stack was not working as I was not running with the dev.Dockerfile build which brings in the zscaler.pem cert to allow SSL connections
- after running the dev.Dockerfile in the docker stack and copying the rety.py and broken_links_to_delete.csv test file for local testing I have tested it successfully with the expected responses in the retry.csv file that was output
- command to run the script on the ckan docker container is - 

`python retry.py ./broken_links.csv /tmp/retry.csv -o orgs.txt`

- next step is to run the retry script on Integration, as it stores it as a separate log file I will run `cat /script/retry.csv` so that it is available as part of the job log for now
- the charts script file will have to be updated to download the check links report and the orgs to defer list
- also the broken links report is actually already filtered for deferred orgs so the retry will have to run against the check_links_report, will remove the broken links and rename the test file to avoid confusion
- after running retry script and downloading the report, I have extracted the csv portion of the script output that will be used to run against the process script
  - 3 links that were previously broken appeared to be working now, but they all appear to point to a draft attachment that sits behind GOV.UK signon page
  - they should probably be still deleted as not available without credentials and still in a draft state.
  - I've asked the question on the NDL team chat to get opinions from technical and product
- next step is to copy over the process script from alphagov/datagovuk-scripts/check-links/process_check_links_report.py and update it so that it can be run as a single file and removed the s3 upload as we will be downloading the report, then test this against the retry script locally against the test data before testing it out on Integration on a dry run
- command to run the process script -

```
python process.py --input ./retried.csv --set-state deleted --output-dir /tmp
```

- NOTE that the retry script must be run before the process script as it also filters for the deferred orgs, then the output from the retry script should be used against the process script
- in order to be able to run the reindex script after the process script the reindex file needs to be predicatable so remove the timestamp part from the reindex filename
- copy over the reindex script from alphagov/ckanext-datagovuk/bin/python_scripts/solr_reindex_package_ids.py and update it to remove references to the FILENAME_BASE as it will be run in charts with args passed in
- command to run the reindex script on the local docker stack is -

```
python reindex.py --input-file /tmp/deleted_packages_to_reindex.txt
```

- the commands to process and reindex the dataset should be run from the same script job
  - next step is to test this out in Integration with a dry run before setting the mode to a live run
- the retry script doesn't check if the resource URL has been updated, so update the code to get the latest URL from the database but also show what the original URL is in the output csv file
- the updated retry script was ran successfully locally and on Integration
- the log file from the job was downloaded and the csv file extracted from it
- the retry csv file indicated that there were 45 resources that were skipped because the resource is now working
- the process file was tested locally and then on Integration, both ran successfully
