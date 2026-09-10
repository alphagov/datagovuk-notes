def is_filter_by(resource, orgs, is_defer_org=False, status_filter_by=None):
    if orgs:
        if is_defer_org and resource["org-name"] in orgs:
            return False
        elif not is_defer_org and resource["org-name"] in orgs:
            return True

    if status_filter_by:
        if resource["http-status"] and str(resource["http-status"]) in status_filter_by:
            return True
        elif resource["category"] in status_filter_by:
            return True
        else:
            return False

    return True
