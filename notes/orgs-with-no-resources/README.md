https://cddodatamarketplace.atlassian.net/browse/DGUK-740

- no built in way to delete orgs from the ckan system, so will have to delete orgs via database and solr calls

- no need for solr call, removing from the database is sufficient for removing the publisher from the CKAN system

- trying this out locally on the docker stack to delete orgs, succesfully set org and related records tto a deleted state

- question is whether we want to permanently delete org records and their related records or just set it to a deleted state
  - permanent deletion will enable those orgs to be recreated with the actual org name and not with suffixes that avoid clashing eg `example-org1` rather than `example-org`
  - setting to a deleted state will allow the org to be undeleted if needed

- after a successful run locally will try it on Integration
  - https://github.com/alphagov/govuk-dgu-charts/tree/try-script is being used to test the script out on Integration, a separate branch will be created once testing on Integration is complete

  - the solr search picked up some datasets which required filtering by the type of package and the state, as there were some draft and harvest package types matched
  
  - some datasets are showing in the old find but not new python app 
    - https://find-only.eks.integration.govuk.digital/search?q=&filters%5Bpublisher%5D=NHS+Airedale%2C+Wharfedale+and+Craven+CCG&filters%5Btopic%5D=&filters%5Bformat%5D=
    - https://www.integration.data.gov.uk/search?query=&publisher=NHS+Airedale%2C+Wharfedale+and+Craven+CCG&topic=&format=

    - blackpool-fylde-wyre-hospitals-nhs-foundation-trust
    https://find-only.eks.integration.govuk.digital/search?q=&filters%5Bpublisher%5D=Blackpool%2C+Fylde+%26+Wyre+Hospitals+NHS+Foundation+Trust&filters%5Btopic%5D=&filters%5Bformat%5D=
    - https://www.integration.data.gov.uk/search?query=&publisher=Blackpool%2C+Fylde+%26+Wyre+Hospitals+NHS+Foundation+Trust&topic=&format=

    They are showing in Staging and production however 
    - https://www.data.gov.uk/search?query=&publisher=NHS+Airedale%2C+Wharfedale+and+Craven+CCG&topic=&format=&sort=best

    - it seems like the changes to drop datasets from search results that have no resources has been deployed to integration which is why they are not showing

    Will check if they are still required to be removed before running the script on Staging and Production

    - The script otherwise ran successfully, next will actually do the deletion

- bit more clarity on the spreadsheet with orgs that have datasets with not resources to be removed
  - so will shift the code to check if there are any resources linked to the org instead
  - the query will be something like this - tested out on my local stack

  ```
  SELECT COUNT(*) FROM resource WHERE state = 'active' AND package_id IN (
    SELECT id FROM package WHERE state = 'active' AND owner_org = '7eb02ff1-61bd-4726-954c-0d4746e1414e'
  );
  ```

- the run on Integration appeared to be successful for the report, will now move deleting the orgs in Integration
  - the publishers are still showing in the drop down list, they need to be removed from the solr index

  - I added the doc in the local solr server - 

  ```
    curl -X POST \
    -d '{"add":{ "doc":{
            "site_id":"dgu_organisations_2",
            "id":"test_id_1",
            "title":"Example Publisher 1",
            "name":"example-publisher-1",
        }}}' \
    -H "Content-Type: application/json" \
    $CKAN_SOLR_URL/update?commit=true    
  ```

  - and then ran the delete orgs script to remove it
