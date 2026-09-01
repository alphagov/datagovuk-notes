https://cddodatamarketplace.atlassian.net/browse/DGUK-740

- no built in way to delete orgs from the ckan system, so will have to delete orgs via database and solr calls

- no need for solr call, removing from the database is sufficient for removing the publisher from the CKAN system

- trying this out locally on the docker stack to delete orgs, succesfully set org and related records tto a deleted state

- question is whether we want to permanently delete org records and their related records or just set it to a deleted state
  - permanent deletion will enable those orgs to be recreated with the actual org name and not with suffixes that avoid clashing eg `example-org1` rather than `example-org`
  - setting to a deleted state will allow the org to be undeleted if needed

- after successful run locally will try it on Integration
