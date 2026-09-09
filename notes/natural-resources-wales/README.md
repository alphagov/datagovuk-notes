## Notes

https://cddodatamarketplace.atlassian.net/browse/DGUK-993

### Investigation into issue 
- https://govuk.zendesk.com/agent/tickets/6222383
- harvest source - https://metadata.naturalresources.wales/geonetwork/gemini/eng/csw
- Doing an initial investigation to try and understand what is going on
- https://metadata.naturalresources.wales/geonetwork/gemini/eng/csw?SERVICE=CSW&VERSION=2.0.2&REQUEST=GetRecords&typeNames=csw:Record&elementSetName=full&maxRecords=500&startPosition=1
  - did not yield any results
- https://metadata.naturalresources.wales/geonetwork/gemini/eng/csw?service=CSW&version=2.0.2&request=GetRecords&resultType=results&typeNames=gmd:MD_Metadata&elementSetName=full&startPosition=1&maxRecords=10
  - 255 records returned
- the run of the harvest on the local docker stack published 20 records, similar to production which has 19, 
  - so the issue is not about what is existing in the current database but points towards an issue on their server

  - example of working record under data/working_nrw_161272.xml
  - example of failing record under data/failing_nrw_100675.xml

  - could use the ckan-mock-harvest-source repo to test fetching data from a harvest source just containing those 2 data sources to see why it is failing
    - to do this we have to capture the call that CKAN is making to the CSW endpoint so that it can be mocked out
    - the location oof the spatial extension on the docker stack is 
    `/usr/lib/ckan/venv/lib/python3.11/site-packages/ckanext/spatial`

    - url 
    
    https://metadata.naturalresources.wales/geonetwork/gemini/eng/csw

    - we need to find out what parameter requests are being made to the csw endpoint so set debug points on the gemini.py file for the CSW harvesting section

    - request 

    ?service=CSW&version=2.0.2&request=GetRecordById&outputFormat=application%2Fxml&outputSchema=http%3A%2F%2Fwww.isotc211.org%2F2005%2Fgmd&elementsetname=full&id=NRW_DS100178

    - checking this request arg with a curl command -

    ```
    curl "https://metadata.naturalresources.wales/geonetwork/gemini/eng/csw?service=CSW&version=2.0.2&request=GetRecordById&outputFormat=application%2Fxml&outputSchema=http%3A%2F%2Fwww.isotc211.org%2F2005%2Fgmd&elementsetname=full&id=NRW_DS102203"
    ```

    - discovered that the code was breaking just after this breakpoint 
    
    `b /usr/lib/ckan/venv/lib/python3.11/site-packages/owslib/iso.py:109`

    - error is
    PT_Locale(i) failing with `AttributeError: 'NoneType' object has no attribute 'attri'`

    - put breakpoint condition for guid NRW_DS161272 - working version, to see why that is passing

    - now trying to locate the call to get all the CSW records, it is in the gemini.py file under the fetch method

    - request url 
    https://metadata.naturalresources.wales/geonetwork/gemini/eng/csw
    - request body
    <csw:GetRecords xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ows="http://www.opengis.net/ows" outputSchema="http://www.isotc211.org/2005/gmd" outputFormat="application/xml" version="2.0.2" service="CSW" resultType="results" maxRecords="10" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-discovery.xsd"><csw:Query typeNames="csw:Record"><csw:ElementSetName>brief</csw:ElementSetName><ogc:SortBy><ogc:SortProperty><ogc:PropertyName>dc:identifier</ogc:PropertyName><ogc:SortOrder>ASC</ogc:SortOrder></ogc:SortProperty></ogc:SortBy></csw:Query></csw:GetRecords>

    - this is what is actually in the urlopen command to retrieve all the records -

    {'data': '<csw:GetRecords xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ows="http://www.opengis.net/ows" outputSchema="http://www.isotc211.org/2005/gmd" outputFormat="application/xml" version="2.0.2" service="CSW" resultType="results" startPosition="10" maxRecords="10" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-discovery.xsd"><csw:Query typeNames="csw:Record"><csw:ElementSetName>brief</csw:ElementSetName><ogc:SortBy><ogc:SortProperty><ogc:PropertyName>dc:identifier</ogc:PropertyName><ogc:SortOrder>ASC</ogc:SortOrder></ogc:SortProperty></ogc:SortBy></csw:Query></csw:GetRecords>', 'json': None, 'headers': {'User-Agent': 'OWSLib (https://geopython.github.io/OWSLib)', 'Content-type': 'text/xml', 'Accept': 'text/xml,application/xml', 'Accept-Language': 'en-US', 'Accept-Encoding': 'gzip,deflate', 'Host': 'metadata.naturalresources.wales'}, 'verify': True, 'cert': None}

    - curl command to get the records

    ```
    curl "https://metadata.naturalresources.wales/geonetwork/gemini/eng/csw" -d '<csw:GetRecords xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ows="http://www.opengis.net/ows" outputSchema="http://www.isotc211.org/2005/gmd" outputFormat="application/xml" version="2.0.2" service="CSW" resultType="results" startPosition="10" maxRecords="300" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-discovery.xsd"><csw:Query typeNames="csw:Record"><csw:ElementSetName>brief</csw:ElementSetName><ogc:SortBy><ogc:SortProperty><ogc:PropertyName>dc:identifier</ogc:PropertyName><ogc:SortOrder>ASC</ogc:SortOrder></ogc:SortProperty></ogc:SortBy></csw:Query></csw:GetRecords>' -H 'Content-Type: text/xml' -H 'Accept text/xml' > natural-resources-wales/data/nsw-all.xml
    ```
    - get the record by id
      - gmd:characterEncoding/gmd:MD_CharacterSetCode element is expected but missing from the records that are failing
      - the error thrown however is a missing `attri` property on `None` object which eventually translates to `Error getting the CSW record with GUID XXX` on the CKAN harvest jobs errors list which is not helpful to publishers and could indicate an issue with our harvest process
    - created a script `get_csw_ids.py` to check how many CSW records are missing
    - create a curl command to independently check each resource held by NRW to see if this matches what is being made available
      - the output from the run was able to identify 246 records, of which only 20 have the correct element
    - to help the publisher check their CSW records I have created a curl command to look specifically for the closed `characterEncoding` element
    ```
curl "https://metadata.naturalresources.wales/geonetwork/gemini/eng/csw?service=CSW&version=2.0.2&request=GetRecordById&outputFormat=application%2Fxml&outputSchema=http%3A%2F%2Fwww.isotc211.org%2F2005%2Fgmd&elementsetname=full&id=NRW_DS100675" | grep "<gmd:characterEncoding />"
    ```
    - the ticket has been updated with information from my investigation and the curl command to help the publisher check their records and submitted as solved
