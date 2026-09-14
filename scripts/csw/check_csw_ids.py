import xml.etree.ElementTree as tree
from urllib.request import urlopen
import ssl
import traceback

from csw_client import CswService


# ============================ zscaler SSL interception workaround ============================
# Use a script to get the CSW identifiers as the zscaler SSL interception is blocking access to the CSW service. The script will download the identifiers and save them to a local file for processing.
# curl "https://metadata.naturalresources.wales/geonetwork/gemini/eng/csw" -d '<csw:GetRecords xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ows="http://www.opengis.net/ows" outputSchema="http://www.isotc211.org/2005/gmd" outputFormat="application/xml" version="2.0.2" service="CSW" resultType="results" startPosition="10" maxRecords="300" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-discovery.xsd"><csw:Query typeNames="csw:Record"><csw:ElementSetName>brief</csw:ElementSetName><ogc:SortBy><ogc:SortProperty><ogc:PropertyName>dc:identifier</ogc:PropertyName><ogc:SortOrder>ASC</ogc:SortOrder></ogc:SortProperty></ogc:SortBy></csw:Query></csw:GetRecords>' -H 'Content-Type: text/xml' -H 'Accept text/xml' > natural-resources-wales/data/nsw-all.xml
_xml = tree.parse("notes/natural-resources-wales/data/nsw-all.xml")
_namespaces = {"gco": "http://www.isotc211.org/2005/gco", "gmd": "http://www.isotc211.org/2005/gmd"}

_ids = []
for elem in _xml.findall(".//gmd:fileIdentifier/gco:CharacterString", _namespaces):
    if elem.text:
        _ids.append(elem.text.strip())

REQUEST_URL = "https://metadata.naturalresources.wales/geonetwork/gemini/eng/csw?service=CSW&version=2.0.2&request=GetRecordById&outputFormat=application%2Fxml&outputSchema=http%3A%2F%2Fwww.isotc211.org%2F2005%2Fgmd&elementsetname=full&id={id}"

# Disable SSL certificate verification for the request to work around zscaler issues. 
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
# =========================== end zscaler SSL interception workaround ============================

csw = CswService(REQUEST_URL)
## if you want to get the identifiers from the CSW service directly. This will make a request to the CSW service to get the identifiers, but may not work due to zscaler SSL interception issues.
# _ids = []
# for id in csw.getidentifiers():
#     _ids.append(id)
# context = ssl.create_default_context()

results = []
exceptions = {}
for i, id in enumerate(_ids):
    print(f"Processing {i+1}/{len(_ids)}: {id}")
    if i > 20: 
        break
    trace_block = ""
    with urlopen(REQUEST_URL.format(id=id), context=context) as req:
        xml = tree.parse(req)
        try:
            csw.getrecordbyid(ids=[id])
        except Exception as e:
            _trace_list = traceback.format_exc().split("\n")
            trace_block = str(_trace_list[-5:])
            if trace_block not in list(exceptions.keys()):
                exceptions[trace_block] = 1
            else:
                exceptions[trace_block] += 1
        results.append((id, trace_block))

print(f"GUIDs that have failed: {','.join(id[0] for id in results)}")

for key, count in exceptions.items():    
    print(f"\n======== Exception\n{key}\n======== count: {count}\n")

num_successful = sum(1 for _, error in results if not error)
print(f"Successful getrecordbyid: {num_successful} / {len(results)}")
