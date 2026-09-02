https://cddodatamarketplace.atlassian.net/browse/DGUK-740

- no built in way to delete orgs from the ckan system, so will have to delete orgs via database and solr calls

- no need for solr call, removing from the database is sufficient for removing the publisher from the CKAN system

- trying this out locally on the docker stack to delete orgs, succesfully set org and related records tto a deleted state

- question is whether we want to permanently delete org records and their related records or just set it to a deleted state
  - permanent deletion will enable those orgs to be recreated with the actual org name and not with suffixes that avoid clashing eg `example-org1` rather than `example-org`
  - setting to a deleted state will allow the org to be undeleted if needed

- after a successful run locally will try it on Integration
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

    - The script otherwise ran successfully, next will actual do the deletion
