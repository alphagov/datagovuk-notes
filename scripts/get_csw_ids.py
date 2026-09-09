import xml.etree.ElementTree as tree
from urllib.request import urlopen
import ssl

_xml = tree.parse("natural-resources-wales/data/nsw-all.xml")
_namespaces = {"gco": "http://www.isotc211.org/2005/gco", "gmd": "http://www.isotc211.org/2005/gmd"}

_ids = []
for elem in _xml.findall(".//gmd:fileIdentifier/gco:CharacterString", _namespaces):
    if elem.text:
        _ids.append(elem.text.strip())

REQUEST_URL = "https://metadata.naturalresources.wales/geonetwork/gemini/eng/csw?service=CSW&version=2.0.2&request=GetRecordById&outputFormat=application%2Fxml&outputSchema=http%3A%2F%2Fwww.isotc211.org%2F2005%2Fgmd&elementsetname=full&id={id}"

# Disable SSL certificate verification for the request to work around zscaler issues. This is not recommended for production use, but is necessary in this case due to the SSL interception by zscaler.
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

results = []
for i, id in enumerate(_ids):
    print(f"Processing {i+1}/{len(_ids)}: {id}")
    found = True
    with urlopen(REQUEST_URL.format(id=id), context=context) as req:
        xml = tree.parse(req)
        for elem in xml.findall(".//gmd:PT_Locale/gmd:characterEncoding", _namespaces):
            if not len(elem.findall("gmd:MD_CharacterSetCode", _namespaces)):
                found = False
        results.append((id, found))

for id, found in results:
    if not found:
        print(f"Dataset {id} does not have correct character encoding")

num_found = sum(1 for _, found in results if found)
print(f"Found {num_found} of {len(results)} datasets with correct character encoding")
