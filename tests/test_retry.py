import resource

from scripts.check_links.lib import is_filter_by


def test_is_filter_none_set():
    orgs = []
    resource = {"org-name": "Org A"}
    assert is_filter_by(resource, orgs, is_defer_org=False) == True


def test_is_filter_by_org():
    orgs = ["Org A"]
    resource = {"org-name": "Org A"}
    assert is_filter_by(resource, orgs, is_defer_org=True) == False
    assert is_filter_by(resource, orgs, is_defer_org=False) == True


def test_is_filter_by_status():
    resource = {"http-status": 404, "category": "TIMEOUT"}
    assert is_filter_by(resource, "", status_filter_by="404") == True
    assert is_filter_by(resource, "", status_filter_by="TIMEOUT") == True
    assert (
        is_filter_by(resource, "", status_filter_by="404,410,TIMEOUT,CONNECTION_ERROR")
        == True
    )


def test_is_filter_by_multiple_statuses():
    resource = {"http-status": 410, "category": "CONNECTION_ERROR"}
    assert (
        is_filter_by(resource, "", status_filter_by="404,410,TIMEOUT,CONNECTION_ERROR")
        == True
    )
    assert is_filter_by(resource, "", status_filter_by="404,TIMEOUT") == False


def test_is_filter_by_category_filters():
    resource = {"http-status": "", "category": "DNS_ERROR"}
    assert (
        is_filter_by(
            resource, "", status_filter_by="404,410,TIMEOUT,DNS_ERROR,CONNECTION_ERROR"
        )
        == True
    )
