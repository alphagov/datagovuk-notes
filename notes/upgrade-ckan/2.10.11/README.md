https://cddodatamarketplace.atlassian.net/jira/software/projects/DGUK/boards/761?filter=textfields%20~%20%22upgrade*%22&groupBy=custom&selectedIssue=DGUK-1048

## Notes

- need to figure out how to build on top of CKAN, could potentially use their dockerhub bas image for CKAN and add to that
  - https://hub.docker.com/r/ckan/ckan-base?tag=2.10.11
- unfortunately we can't build this using the existing dockerhub immage as it is not built in ARM64
- tried to build it using our existing Dockerfile files but I very quickly hit dependency issues which was proving very difficult to untangle
- so I decided to build the base ourselves 
`docker build -t localhost:59247/ckan-base:2.10.11 -f docker/ckan/ckan-base.Dockerfile docker/ckan --build-arg CKAN_REF=ckan-2.10.11`
- once this was built, the extensions were built on top of this
  - various mappings had to change in the Dockferfile as it is being built differently
`docker build -t localhost:59247/dgu-base:2.10.11 -f docker/ckan/dgu-base.Dockerfile docker/ckan`
- the ckanext-datagovuk build was done with some further changes to the Dockerfile
  - the dev build was moved into this Dockerfile so that it is in line with how CKAN are using their Dockerfile
  `docker build -t localhost:59247/ckan:2.10.11 -f docker/ckan/2.10.11.Dockerfile . --build-arg ENV=dev `
  - the dev build has been used much more whilst I am trying to fix the Dockerfile builds
  - `docker-compose-2.10.yml` file was also updated to run with the new `ckan.ini` file, this replaces the existing `production.ini` file
  - after resolving a number of dependency issues I have managed to get CKAN running locally with some issues around the theming and a warning around `flask_multistatic` library, this library is not supported in the latest Flask versions but migrating to a later flask version causes other dependency issues
- checklist for running CKAN
  - search reindex working
  - styling to inline with existing prod deployment
  - organograms are working
  - harvesting is working
  - user login is working
  - user management is working for admins
  - update the github actions to work with the ckan-base, dgu-base and dgu-final Dockerfiles
    - update the workflow to only target the specific dockerfiles and not have the version as part of the Dockerfile
      - separate the workflow out initially and trigger on push to the upgrade branch
      - after building these on GHCR then can use them on the local cluster
  - deployment to local cluster is working
- the search index rebuild successfully completed after ignoring indexing errors 
` ckan search-index rebuild -i`
- there is an issue with the resource plugin override not being picked up, the `data` field should be populated in `package/snippets/resource_form.html` in the `ckanext-datagovuk` repo but it is not being set so the upload file button is not being rendered.
  - so I have decided to create another docker app which pulls down the 2.10.7 image to compare with the 2.10.11 docker app in the docker-compose file
  - run ckan to allow breakpoints - `ckan run --passthrough-errors -H 0.0.0.0`
  - need to understand why uploads_enabled() for 2.10.7 but not 2.10.11 
  - the buttons are enabled for 2.10.11 build, the configuration was missing the `ckan.uploads_enabled` set to `true`
  - some further basic testing was done and reached the point at uploading to the s3 bucket where it will fail as it is not connected to s3
    - did a quick trial of some docker s3 mock images but they do not have all the s3 features needed to get the upload working
- 
