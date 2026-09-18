def filter_resource(resource, deferred_orgs, statuses=None, domains=None):
    if deferred_orgs and resource["org-name"] in deferred_orgs:
        return False

    if domains and any(domain in resource["resource-url"] for domain in domains):
        return True

    if statuses:
        has_status = resource["http-status"] and str(resource["http-status"]) in statuses
        has_category = resource["category"] and resource["category"] in statuses
        if has_status or has_category:
            return True
        else:
            return False

    if not statuses and not domains:
        return True

    return False
