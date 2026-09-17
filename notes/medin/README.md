https://cddodatamarketplace.atlassian.net/issues?jql=textfields%20~%20%22medin*%22&wildcardFlag=true&selectedIssue=DGUK-926

## Notes

- The script to create the list of datasets that are not published is - 

```sql
COPY (
with medin (guid) as (
   VALUES ('01456949c2f8576182af30d432d86b9c'),('03d046b98ee0557a980578eb38da4b35'), ...
)
select medin.guid FROM medin 
WHERE medin.guid NOT IN (
    SELECT guid FROM harvest_object where 
harvest_source_id = '885ee504-c712-4f8d-9034-1c230bcd88a6' 
AND report_status IN ('added', 'not modified', 'updated')
AND guid in ('01456949c2f8576182af30d432d86b9c','03d046b98ee0557a980578eb38da4b35','052af652214b57e1b2137c8478bcacf4', ...)
)
) To STDOUT \g /tmp/medin_not_published.csv
```

- harvest source url: https://portal.medin.org.uk/keyword_search/NDGO0005/
  - gemini WAF
    - this means that we can go to the url directly to grab the IDs
- created a `check_waf_ids.py` script which autogenerates the SQL script to run for checking the list of duplicates not published
  - using the script on Integration it identified 73 guids which are not being published, see medin_not_published-160926.csv
  - using these 73 guids, get the list of errors from the harvest_object_error table

  ```sql
  COPY (
  SELECT harvest_object_id, message, stage FROM harvest_object_error WHERE harvest_object_id IN 
  (SELECT id FROM harvest_object WHERE gathered >= '2026-09-09' AND gathered <= '2026-09-11' AND guid IN ('CEFAS00579afa-6240-4387-bddc-0af787b17ad2','CEFAS02be0911-ac86-4a50-9174-8e61b660e29c','CEFAS04957bea-5e56-4edc-9b3b-51e9a7ba85d7','CEFAS079fe9bb-b471-4fa9-87fe-c04038ed85cf','CEFAS0982e695-2683-468e-a0ac-b6278764235b','CEFAS0e09fcb5-0495-44be-8d85-fbd903e61372','CEFAS13f7856a-a7a9-4a5f-b32e-ebe4570049eb','CEFAS15aabafe-79df-4f58-a53e-6a25628948f9','CEFAS18b7512b-7f5a-4e74-af8a-5b8bd512ac23','CEFAS19ae81d5-a98f-4465-babd-a506a5628a48','CEFAS1ce83ce7-3d64-486a-b5e1-ff514e566a25','CEFAS1e8cf53d-fa73-411d-b827-5c2f110735b9','CEFAS208d5047-484f-4ff8-be5b-944673c88791','CEFAS214168bf-0ccb-4ebd-ae43-8ea9d413d76e','CEFAS23de6638-2f10-4083-a9fa-b4c66785da63','CEFAS298f6cc9-19f2-4c6d-b4e5-60adbd377fd3','CEFAS2c11a431-5d0d-471e-8ade-98d6e9d1663b','CEFAS2d3352dd-a679-48cb-82ba-50a38bf6740a','CEFAS33eb1840-7872-4f3f-ab3f-62ed4539d1d9','CEFAS3490ce6c-3432-499f-9906-294a5d4f5ba8','CEFAS3ceffabf-f857-4fdc-bfce-c478899c3b8a','CEFAS3de8da1f-87a3-4fbf-a3bc-3e4c6473fa47','CEFAS4296fa91-8078-4f25-bab6-5d48374107d2','CEFAS480e7a76-7166-4e93-8a3e-839e0936d0fc','CEFAS55b51c1c-c7e9-4678-98aa-e47d91a7979f','CEFAS582d5efc-9c56-48f1-b543-7dcea736bc74','CEFAS5bda80e5-9d81-4d90-bc8f-dc1c844fa1db','CEFAS5d267b6b-f275-48e5-ba06-434e23384662','CEFAS65f1b9d1-27f8-492f-a8f2-8394634bb6b8','CEFAS68836eaf-4f54-46b7-ae95-e56a0ade1963','CEFAS6a773390-f2d4-4dd8-a869-906c8b8165b4','CEFAS6bcb8439-c1e4-42f2-8ef4-97f8d0dc54f8','CEFAS6e921427-db10-4619-be2d-06552782d6f6','CEFAS71580633-9331-4b82-9506-eb2dc7361c2d','CEFAS71e7d71e-3b0e-4d4e-b678-04678689f3c4','CEFAS7282f3b6-7dd2-48f8-b999-dc70546d14ab','CEFAS76e70ba8-09d1-452d-83a4-19e2412a72af','CEFAS7b92ea85-8616-40ae-9abe-01154e8f875a','CEFAS7c1d97b9-926b-4b5d-93c1-93293990d6a9','CEFAS7c5ae7d0-6d4f-485f-b110-b46b43682869','CEFAS82484202-485a-45e6-8caa-e8658ebf1ee2','CEFAS83a0c9c4-6d47-4e3a-838b-179effb361e8','CEFAS8596988c-67f3-49a5-9e34-86242f314c82','CEFAS885b264a-a63c-429e-952c-5a4cd1b06a6c','CEFAS8aa9c974-9199-41eb-a7c7-05c4feaf2591','CEFAS8b57c2b8-8f31-4d50-80e9-1b7884df8fd0','CEFAS8f78a8b9-e1b5-417b-a12f-5c813ae55b76','CEFAS912c2eaa-f99d-4114-b627-a6d988530519','CEFAS9374261c-7767-4e5c-9293-0986895ec7f6','CEFAS93d5838b-b4e1-45cb-99eb-e1317a8fb004','CEFAS984c2691-a725-459a-8c88-18134c1e7b7a','CEFAS9e8df82d-40b6-4931-9a77-3c72d3af82d8','CEFASa48a34c3-be97-41ec-ab63-afb92d9d1b53','CEFASa4906784-6b0e-418e-97b2-b7f93305c8ac','CEFASac930b40-121a-4032-beb3-8482b8356a97','CEFASb1a3d524-14d4-40ed-a84b-e3f2acd41619','CEFASb26ec168-92bf-4389-9e89-1070f9ba59cf','CEFASb44fd6bc-7878-4ed3-8c4c-339c322bb4dd','CEFASc0860b3e-7849-44a3-adcc-c9bebdd4af1f','CEFASc220f201-444f-4214-a9d0-6b4bd5cce095','CEFASd316e93a-df6a-4fce-a344-a1e841d31ad5','CEFASd3508275-f6a6-4164-a61a-c6a1b7e6dd78','CEFASda17ac7a-d6bd-45f2-8d69-cd77cc49d575','CEFASde383d26-9a43-4ee0-a116-f15781fe5547','CEFASe147dcef-591e-4209-b2f1-3458d95351cb','CEFASea92dbe1-1000-40d7-b27f-a11221aa14be','CEFASf25f2070-48e0-449a-96ff-9ede0c15bb0a','CEFASf55d404c-d97c-421a-834d-209911d71141','CEFASf7e92c40-8bdb-403a-930c-349c1d8e3d30','CEFASf99e220f-b5d8-4642-93c9-b45d4d07712f','CEFASfc6e0c90-9c1d-4e26-8afa-58ad39c7296a','b0a48b2d-21cb-40c5-a4ad-cb1c2974ccfb','c2a2d863-ac98-4cca-8f2b-28aaa20c0d11'))
  ) To STDOUT \g /tmp/harvest_object_errors.csv
  ```

  - some schema validation error which should not cause the harvest object to be not published but also other obscure errors probably coming from the system
    - will be targeting the range of guids to investigate during a harvest run on test, to speed it up will skip the other guids
    - this didn't reveal any issues with the guids which are not being harvested on production, in fact some datasets were created on the test stack
- ran the `check.sql` script produced by the `check_waf_ids.py` script on Integration
  - looks like these guids are being published by Centre for Environment, Fisheries & Aquaculture Science (CEFAS)
  - the `medin_guids.csv` output file was copied off integration and checked against the list of IDs from the `waf.html` file, there was 1 guid which appears to be missing from the guids published in the database.
    - `SELECT * FROM harvest_object WHERE guid = 'b0a48b2d-21cb-40c5-a4ad-cb1c2974ccfb';` gave an empty result

  - so it looks like all the guids from the MEDIN WAF harvest endpoint are accounted for except for 1 guid - `b0a48b2d-21cb-40c5-a4ad-cb1c2974ccfb`
    - ran a query on production to find it returns an empty result set, perhaps it was added after the last harvest run which was on 10th September
  - the zendesk ticket for MEDIN has been responded with the `medin_guids.csv` file attached so that the publisher can review and understand why some datasets are not showing under their publisher filter
    - also identified that there is a discrepancy between what is shown on CKAN and data.gov.uk for MEDIN initially because there are over 1000 datasets which do not have resources as part of the dataset, these are being omitted from the search results by default
    - the zendesk ticket has been closed as solved but there might be an ask to delete the CEFAS datasets to allow the MEDIN datasets to be harvested instead
