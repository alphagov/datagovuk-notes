https://cddodatamarketplace.atlassian.net/browse/DGUK-1206

## Summary

### Key finding

Between 9 and 12th November there weere 89 access of the senior csv file and 63 requests for the junior csv file. This file contained some sensitive personal data and was deleted by the publisher on the CKAN admin site. However although it was deleted the organogram resource was still publicly available from the s3 bucket, this was eventually set to be not publicly available on the 20th November as currently the deletion of objects for the temporary admin AWS role is not allowed.

### Actions to take forward

Do not allow direct access to the s3 object, instead the object should be accessed indirectly via a link on the data.gov.uk site. A Jira ticket has been created to track this action which will be carrried out when the s3 content is migrated to the NDL AWS accounts.

## Notes

- cannot bulk download the access logs from s3
- this repo might be able to do the job - https://github.com/Ucnt/aws-s3-downloader
  - ./download_bucket.py -n govuk-production-aws-logging -d -x -i s3/datagovuk-production-ckan-organogram/2026-11-09
  - abandoned this script as it was outdated and would require too much work to work as I needed
- created a new script `scripts/s3/download_files.py` that downloads the files in a bucket matching a prefix
- after running the script I ran this search on the downloaded files
  - organogram-department-of-health/resources/2026-11-09T02-14-58Z-2026-09-30-organogram-senior.csv 
    - 89 separate requests for senior file over 56 different IP addresses - 63 for junior over 46 different IP addresses
