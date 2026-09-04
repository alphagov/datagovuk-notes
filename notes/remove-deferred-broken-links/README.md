https://cddodatamarketplace.atlassian.net/browse/DGUK-964 part 2

- extracted broken link resources to delete from spreadsheet `2026 06 Broken links responses` as there was some PII in the doc.
- orgs confirmeed to delete broken link resources - 
    dartmoor-national-park-authority
    department-for-transport
    nhs-blood-and-transplant
    office-of-rail-and-road
    plymouth-city-council
- the script was updated to check if an org was to be processed in the check_links_report
- retry script was also brought in and updated to allow for targets orgs
- the broken_links_to_delete file was copied over as according to the timestamp that was the latest file generated
- initially the CKAN in the docker stack was not working as I was not running with the dev.Dockerfile build which brings in the zscaler.pem cert to allow SSL connections
- after running the dev.Dockerfile in the docker stack and copying the rety.py and broken_links_to_delete.csv test file for local testing I have tested it successfully with the expected responses in the retry.csv file that was output
- command to run the script on the ckan docker container is - 

`python retry.py ./broken_links.csv /tmp/retry.csv -o orgs.txt`

- next step is to run the retry script on Integration, as it stores it as a separate log file I will run `cat /script/retry.csv` so that it is available as part of the job log for now
