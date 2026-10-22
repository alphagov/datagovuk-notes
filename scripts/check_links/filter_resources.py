import argparse
import csv
import time

from .lib import filter_resource


def resources_to_filter(csv_path):
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []

        for row in reader:
            if row["to-delete"].lower() == "false" and row["category"] != "OK" and row["http-status"] != "200":
                rows.append(row)
        return rows

def main(
    input_csv_file_path,
    output_csv_file_path,
    deferred_orgs_path=None,
    status_filter_by=None,
    domains_path=None,
):
    deferred_orgs = []
    if deferred_orgs_path:
        with open(deferred_orgs_path, "r") as f:
            deferred_orgs = [line.strip() for line in f]
        print(f"Filtering out deferred orgs: {deferred_orgs} \n")

    domains = []
    if domains_path:
        with open(domains_path, "r") as f:
            domains = [line.strip() for line in f if line.strip()]
        print(f"Filtering by domains: {domains} \n")

    filters = [f.strip() for f in status_filter_by.split(",")] if status_filter_by else []
    if filters:
        print(f"Filtering resources by {status_filter_by} \n")

    print("Setting filtered resources to-delete = true \n")

    filtered_resources = []
    status_counts = {}
    category_counts = {}

    for resource in resources_to_filter(input_csv_file_path):
        if filter_resource(
            resource,
            deferred_orgs,
            statuses=status_filter_by,
            domains=domains,
        ):
            resource.update({"to-delete": "true"})
            filtered_resources.append(resource)

            status = resource["http-status"]
            category = resource["category"]
            if status in filters:
                status_counts[status] = status_counts.get(status, 0) + 1
            if category in filters:
                category_counts[category] = category_counts.get(category, 0) + 1

    if filters:
        print(f"Filtered resources count by status: {status_counts} \n")
        print(f"Filtered resources count by category: {category_counts} \n")
    print(f"Total filtered resources: {len(filtered_resources)} \n")

    with open(output_csv_file_path, "w", newline="", encoding="utf-8") as f:
        REPORT_HEADERS = [
            "datagovuk-url",
            "package-id",
            "package-name",
            "package-metadata-created",
            "package-metadata-modified",
            "guid",
            "resource-id",
            "resource-url",
            "resource-created",
            "resource-last-modified",
            "resource-metadata-modified",
            "org-name",
            "org-id",
            "http-status",
            "category",
            "error-detail",
            "original-url",
            "original-http-status",
            "original-category",
            "original-error-detail",
            "to-delete",
            "checked-at",
        ]
        writer = csv.DictWriter(f, fieldnames=REPORT_HEADERS, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(filtered_resources)


def parse_args():
    parser = argparse.ArgumentParser(
        description="A script for retrying requests to broken links for data.gov.uk"
    )
    parser.add_argument(
        "input_csv_file_path",
        type=str,
        help="The CSV file of a previous link check/retry run",
    )
    parser.add_argument(
        "output_csv_file_path", type=str, help="Path for CSV file to save results to"
    )
    parser.add_argument(
        "-o",
        "--deferred-orgs-path",
        type=str,
        default=None,
        help="Deferred orgs to filter out (newline separated list of org IDs)",
    )
    parser.add_argument(
        "-d",
        "--domains-path",
        type=str,
        default=None,
        help="Path to a text file of domains to filter by (newline separated)",
    )
    parser.add_argument(
        "-s",
        "--status-filter-by",
        type=str,
        default="",
        help="Status code or category to filter by (default: empty, meaning no filter)",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    start = time.time()
    print("Filtering links...")
    args = parse_args()
    main(
        args.input_csv_file_path,
        args.output_csv_file_path,
        deferred_orgs_path=args.deferred_orgs_path,
        status_filter_by=args.status_filter_by,
        domains_path=args.domains_path,
    )
    time_taken = time.time() - start
    print(f"All links filtered successfully in {time_taken}S.")
