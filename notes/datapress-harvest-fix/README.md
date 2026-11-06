# Notes

Ticket: [DGUK-1020](https://cddodatamarketplace.atlassian.net/browse/DGUK-1020?atlOrigin=eyJpIjoiNmE0NjcyYzFkOTczNGU3MWEzYmE4N2MwYTk4NjUyYTciLCJwIjoiaiJ9)

> We have multiple datapress harvest sources, they are all broken (eg no URLs), using an old, undocumented api endpoint

> [This PR](https://github.com/alphagov/datagovuk-scripts/pull/17) converted the failing harvest source data to be compatible with our CKAN. We need to update harvest sources to point to these [outputs](https://github.com/alphagov/datagovuk-scripts/tree/main/harvest-api-converter/output).

## Summary

We updated the harvest source url for:

1. London Datastore - GLA (greater-london-authority)
    - increased from 1296 datasets to 1304 datasets
2. Open Barnet (london-borough-of-barnet)
    - increased from 391 datasets to 397 datasets
3. Calderdale Dataworks (in progress)
    - increased from 252 datasets to 277 datasets

We cleared the harvest sources for:

1. Datamill North - Durham (durham-county-council)
2. Data Mill North - Leeds (leeds-city-council)
3. Data Mill North - Newcastle (newcastle-city-council )
4. North Tyneside council - DMN (north-tyneside)
5. Stockport Council - Data Mill North (stockport)
6. Sunderland council - Data Mill North (sunderland-city-council)
7. wakefield-dmn (wakefield)

We created a new publisher, `Data Mill North` and added a new harvest source called `data-mill-north` with a url pointing to [data-mill-north-dcat.json](https://raw.githubusercontent.com/alphagov/datagovuk-scripts/refs/heads/main/harvest-api-converter/output/data-mill-north-dcat.json) ([found here](https://github.com/alphagov/datagovuk-scripts/blob/main/harvest-api-converter/output/data-mill-north-dcat.json)) that contains the same datasets that the 7 harvest sources above have.

We reindexed the organisations so that it's available in data.gov.uk/search as a new publisher to filter by.

### Decisions

In order to prevent duplicated datasets for Data Mill North, we had to clear the 7 pre-existing harvest sources.

We cleared them instead of deleted them as a quick, less destructive, move forward.

We then reharvested the new `data-mill-north` harvest source, which re-added the same datasets that those 7 sources had.

### Data Mill North harvest sources

1. Datamill North - Durham (durham-county-council)

2. Data Mill North - Leeds (leeds-city-council)

3. Data Mill North - Newcastle (newcastle-city-council )

4. North Tyneside council - DMN (north-tyneside)

5. Stockport Council - Data Mill North (stockport)

6. Sunderland council - Data Mill North (sunderland-city-council)

7. wakefield-dmn (wakefield)

### Other harvest sources to update

The url for these three harvest sources were updated individually to point to those in [harvest-api-converter/output](https://github.com/alphagov/datagovuk-scripts/tree/main/harvest-api-converter/output) using specifically their raw github url e.g. [calderdale-dcat.json](https://raw.githubusercontent.com/alphagov/datagovuk-scripts/refs/heads/main/harvest-api-converter/output/calderdale-dcat.json)

1. London Datastore - GLA (greater-london-authority)
2. Open Barnet (london-borough-of-barnet)
3. Calderdale Dataworks (in progress)

### Left to do (Tech debt)

- [ ] Delete the 7 data mill north harvest sources that now have 0 datasets
    - Datamill North - Durham (durham-county-council)
    - Data Mill North - Leeds (leeds-city-council)
    - Data Mill North - Newcastle (newcastle-city-council)
    - North Tyneside council - DMN (north-tyneside)
    - Stockport Council - Data Mill North (stockport)
    - Sunderland council - Data Mill North (sunderland-city-council)
    - wakefield-dmn (wakefield)

We'd need to discuss whether or not this is worth doing and how to peroperly delete the harvest source so it doesn't get reintroduced.