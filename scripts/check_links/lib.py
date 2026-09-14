def filter_resource(resource, deferred_orgs, statuses=None):
    if deferred_orgs:
        if resource["org-name"] in deferred_orgs:
            return False

    if statuses:
        if resource["http-status"] and str(resource["http-status"]) in statuses:
            return True
        elif resource["category"] in statuses:
            return True
        else:
            return False

    return True
