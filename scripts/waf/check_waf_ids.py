from bs4 import BeautifulSoup, SoupStrainer

ids = []

with open("notes/medin/waf.html", "r") as f:
    for link in BeautifulSoup(f.read(), 'html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            ids.append(link['href'][4:-4]) # remove leading nnn_ and trailing .xml

print(ids)

SQL = f"""
COPY (
select guid, package_id, "group".name FROM harvest_object, package, "group" WHERE 
package_id = package.id AND "group".id = owner_org AND publisher_id = "group".id AND package.state = 'active'
AND guid in ('{'\',\''.join(ids)}')
GROUP BY guid, package_id, "group".name ORDER BY "group".name, guid
) To STDOUT  With CSV HEADER \g /tmp/medin_guids.csv
"""

with open("notes/medin/check.sql", "w") as f:
    f.write(SQL)
