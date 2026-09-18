from scripts.check_links.lib import filter_resource


def test_filter_resource_no_deferred_orgs():
    deferred_orgs = []
    resource = {"org-name": "Org A"}
    assert filter_resource(resource, deferred_orgs) == True


def test_filter_resource_filters_out_deferred_org():
    deferred_orgs = ["Org A"]
    resource = {"org-name": "Org A"}
    assert filter_resource(resource, deferred_orgs) == False


def test_filter_resource_by_statuses():
    resource = {"http-status": 404, "category": "TIMEOUT"}
    assert filter_resource(resource, deferred_orgs=[], statuses="404") == True
    assert filter_resource(resource, deferred_orgs=[], statuses="TIMEOUT") == True
    assert (
        filter_resource(resource, deferred_orgs=[], statuses="404,410,TIMEOUT,CONNECTION_ERROR")
        == True
    )


def test_filter_resource_multiple_statuses():
    resource = {"http-status": 410, "category": "CONNECTION_ERROR"}
    assert (
        filter_resource(resource, deferred_orgs=[], statuses="404,410,TIMEOUT,CONNECTION_ERROR")
        == True
    )
    assert filter_resource(resource, deferred_orgs=[], statuses="404,TIMEOUT") == False


def test_filter_resource_by_status_category():
    resource = {"http-status": "", "category": "DNS_ERROR"}
    assert (
        filter_resource(
            resource, deferred_orgs=[], statuses="404,410,TIMEOUT,DNS_ERROR,CONNECTION_ERROR"
        )
        == True
    )

def test_filter_resource_deferred_orgs_and_statuses():
    deferred_orgs = ["Org A"]
    resource = {"org-name": "Org B", "http-status": 404, "category": "TIMEOUT"}

    assert filter_resource(resource, deferred_orgs=deferred_orgs, statuses="404,TIMEOUT") == True


def test_filter_resource_domains_without_statuses():
    resource = {"org-name": "Org A", "resource-url": "https://example.com/test", "http-status": 200, "category": ""}

    assert filter_resource(resource, deferred_orgs=[], domains=["example.com"]) == True
    assert filter_resource(resource, deferred_orgs=[], domains=["other.com"]) == False
