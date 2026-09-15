def filter_resource(resource, deferred_orgs, statuses=None, domains=None):
    if deferred_orgs and resource["org-name"] in deferred_orgs:
        return False

    if domains and any(domain in resource["resource-url"] for domain in domains):
        return True

    if statuses:
        if resource["http-status"] and str(resource["http-status"]) in statuses or resource["category"] in statuses:
            return True
        else:
            return False

    return False
