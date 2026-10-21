import csv

from scripts.check_links.filter_resources import main as filter_resources


def test_filter_resources_by_status_excludes_deferred_and_successful_resources(tmp_path):
    output_path = tmp_path / "filtered_check_links_report.csv"

    filter_resources(
        "notes/delete-broken-links-to-delete-false/test_data/check_links_report.csv",
        output_path,
        "notes/delete-broken-links-to-delete-false/test_data/orgs-to-defer.txt",
        status_filter_by="401",
    )

    with output_path.open(newline="") as csvfile:
        rows = list(csv.DictReader(csvfile))

    assert len(rows) == 1
    assert all(row["org-name"] == "example-publisher-2" for row in rows)
    assert all(row["to-delete"] == "true" for row in rows)
    assert (rows[0]["http-status"], rows[0]["category"]) == ("401", "")


def test_filter_resources_excludes_to_delete_true_rows(tmp_path):
    output_path = tmp_path / "filtered_check_links_report.csv"

    filter_resources(
        "notes/delete-broken-links-to-delete-false/test_data/check_links_report.csv",
        output_path,
        "notes/delete-broken-links-to-delete-false/test_data/orgs-to-defer.txt",
        status_filter_by="DNS_ERROR,401",
    )

    with output_path.open(newline="") as csvfile:
        rows = list(csv.DictReader(csvfile))

    assert all(row["to-delete"] == "true" for row in rows)


def test_filter_resources_excludes_200_status(tmp_path):
    output_path = tmp_path / "filtered_check_links_report.csv"

    filter_resources(
        "notes/delete-broken-links-to-delete-false/test_data/check_links_report.csv",
        output_path,
        "notes/delete-broken-links-to-delete-false/test_data/orgs-to-defer.txt",
        status_filter_by="200",
    )

    with output_path.open(newline="") as csvfile:
        rows = list(csv.DictReader(csvfile))

    assert len(rows) == 0


def test_filter_resources_excludes_deferred_orgs(tmp_path):
    output_path = tmp_path / "filtered_check_links_report.csv"

    filter_resources(
        "notes/delete-broken-links-to-delete-false/test_data/check_links_report.csv",
        output_path,
        "notes/delete-broken-links-to-delete-false/test_data/orgs-to-defer.txt",
        status_filter_by="DNS_ERROR,401",
    )

    with output_path.open(newline="") as csvfile:
        rows = list(csv.DictReader(csvfile))

    assert all(row["org-name"] != "example-publisher-1" for row in rows)
