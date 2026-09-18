
## Step 1

This is to filter the resources:

- Filter by to-delete=false
- Filter out http-status=200s
- Filter out deferred orgs
- Filter by http-status / http-category of: `404,410,TIMEOUT,CONNECTION_ERROR,SERVER_ERROR,DNS_ERROR`

Ran the below command

```bash
python3 scripts/check_links/filter_resources.py \
  -s "404,410,TIMEOUT,CONNECTION_ERROR,SERVER_ERROR,DNS_ERROR" \
  -o notes/delete-broken-links-to-delete-false/orgs-to-defer.txt \
  notes/delete-broken-links-to-delete-false/errors-current.csv \
  scripts/check_links/step1_filter_resources_result.csv
```

The input CSV was `errors-current.csv`
The output CSV is `step1_filter_resources_result.csv` which contains the filtered resources

### Printed out statistics for Integration

```bash
  Filtering links...
  Filtering out deferred orgs: ['healthcare-quality-improvement-partnership', 'newcastle-city-council', 'rural-payments-agency', 'royal-borough-of-kensington-and-chelsea', 'leicester-city-council', 'healthcare-quality-improvement-partnership', 'marine-environmental-data-information-network', 'nottingham-city-council', 'national-highways', 'bridgend-county-borough-council', 'oxford-city-council', 'wirral-metropolitan-borough-council', 'environment-agency', 'marine-management-organisation', 'natural-england', 'department-for-environment-food-and-rural-affairs', 'animal-and-plant-health-agency'] 

  Filtering resources by 404,410,TIMEOUT,CONNECTION_ERROR,SERVER_ERROR,DNS_ERROR 

  Setting filtered resources to-delete = true 

  Filtered resources count by status: {'404': 3062, '410': 2} 

  Filtered resources count by category: {'CONNECTION_ERROR': 2410, 'SERVER_ERROR': 1353, 'TIMEOUT': 7968, 'DNS_ERROR': 548} 

  Total filtered resources: 15343 

  All links filtered successfully in 0.43290281295776367S.
```


## Step 2

This is similar to step 1 but it filters by invalid domains and does not filter by status.

- Filter by to-delete=false
- Filter out http-status=200s
- Filter out deferred orgs
- Filter by invalid domains

```bash
 python3 scripts/check_links/filter_resources.py \
    -o notes/delete-broken-links-to-delete-false/orgs-to-defer.txt \
    -d notes/delete-broken-links-to-delete-false/domains-to-delete.txt \
    notes/delete-broken-links-to-delete-false/errors-current.csv \
    notes/delete-broken-links-to-delete-false/step2_filtered_resources_by_invalid_domains.csv
```

```bash
  Filtering links...
  Filtering out deferred orgs: ['healthcare-quality-improvement-partnership', 'newcastle-city-council', 'rural-payments-agency', 'royal-borough-of-kensington-and-chelsea', 'leicester-city-council', 'healthcare-quality-improvement-partnership', 'marine-environmental-data-information-network', 'nottingham-city-council', 'national-highways', 'bridgend-county-borough-council', 'oxford-city-council', 'wirral-metropolitan-borough-council', 'environment-agency', 'marine-management-organisation', 'natural-england', 'department-for-environment-food-and-rural-affairs', 'animal-and-plant-health-agency'] 

  Filtering by domains: ['geoportal1-ons.opendata.arcgis.com', 'opendata-daerani.hub.arcgis.com', 'inspire.misoportal.com', 'opendata-nstauthority.hub.arcgis.com', 'osni-spatialni.opendata.arcgis.com', 'data.barrowbc.gov.uk', 'itportal.decc.gov.uk', 'uploads.scarborough.gov.uk', 'data.peterborough.gov.uk', 'gmtu.gov.uk', 'data.horsham.gov.uk', 'sfo.gov.uk', 'pendle.gov.uk', 'maps.northlincs.gov.uk', 'rcplondon.ac.uk', 'ccg.nhs.uk'] 

  Setting filtered resources to-delete = true 

  Total filtered resources: 13796 

  All links filtered successfully in 0.42493629455566406S.
```
