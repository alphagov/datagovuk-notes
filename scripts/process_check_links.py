"""Process a check_links.py CSV report.

This script marks resources as deleted ('inactive') or
active in the database depending on the `--set-state` flag which
accepts the values `deleted` or `actove`.

The default `--mode`, dry-run, will not make any database
updates. It only update resources if run in live mode.

This does NOT fetch resources from the database or
check link liveness, it uses the report and actions it directly.

Use it to apply a previously generated report without rerunning the
resource liveness check

Writes a `packages_to_reindex_apply_{ts}.txt` for feeding into
`solr_reindex_package_ids.py`.
"""

import argparse
import contextlib
import csv
import logging
import os
import psycopg2
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent))


LOG_FILE = "check_links_updated_to_{state}.log"
REINDEX_FILE = "{state}_packages_to_reindex_{timestamp}.txt"


@dataclass(frozen=True)
class ResourceRow:
    """Represents a package (dataset) resource and its URL from db"""

    package_id: str
    package_name: str
    resource_id: str
    url: str
    org_name: str | None = None
    org_id: str | None = None
    resource_created: datetime | None = None
    resource_last_modified: datetime | None = None
    resource_metadata_modified: datetime | None = None
    package_metadata_created: datetime | None = None
    package_metadata_modified: datetime | None = None
    guid: str | None = None


class Repository:
    """Handles all db access. One connection opened in __enter__."""

    SELECT_SQL = """
        WITH harvest_objects_by_package_id AS (
            SELECT package_id, guid
            FROM harvest_object
            GROUP BY package_id, guid
        )
        SELECT p.id, p.name, r.id, r.url, g.name as org_name, g.id as org_id,
               r.created as resource_created,
               r.last_modified as resource_last_modified,
               r.metadata_modified as resource_metadata_modified,
               p.metadata_created as package_metadata_created,
               p.metadata_modified as package_metadata_modified,
               ho.guid as guid
        FROM package p
        JOIN resource r ON r.package_id = p.id
        LEFT JOIN "group" g on p.owner_org = g.id
        LEFT JOIN harvest_objects_by_package_id AS ho ON p.id = ho.package_id
        WHERE p.state = 'active'
          AND p.type = 'dataset'
          AND r.state = 'active'
          AND r.url IS NOT NULL
          AND TRIM(r.url) <> ''
        ORDER BY p.id, r.id
    """
    UPDATE_RESOURCE_SQL = "UPDATE resource SET state = 'deleted' WHERE id = %(resource_id)s AND state = 'active'"
    UPDATE_RESOURCE_ACTIVE_SQL = "UPDATE resource SET state = 'active' WHERE id = %(resource_id)s AND state = 'deleted'"
    UPDATE_PACKAGE_MTIME_SQL = (
        "UPDATE package SET metadata_modified = NOW() WHERE id = %(package_id)s"
    )

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._conn: psycopg2.extensions.connection | None = None

    def __enter__(self):
        self._conn = psycopg2.connect(self._dsn)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def fetch_resources(self, limit: int | None = None) -> list[ResourceRow]:
        # TODO: positional unpacking of cursor is getting a bit shonky. circle back later
        # possibly switch to NamedTupleCursor or DictCursor? might need some more aliases
        # to avoid name clashes
        assert self._conn is not None, "Repository not entered"
        with self._conn, self._conn.cursor() as cur:
            if limit is not None:
                cur.execute(self.SELECT_SQL + " LIMIT %s", (limit,))
            else:
                cur.execute(self.SELECT_SQL)
            return [
                ResourceRow(
                    package_id=package_id,
                    package_name=package_name,
                    resource_id=resource_id,
                    url=url.strip(),
                    org_name=org_name,
                    org_id=org_id,
                    resource_created=resource_created,
                    resource_last_modified=resource_last_modified,
                    resource_metadata_modified=resource_metadata_modified,
                    package_metadata_created=package_metadata_created,
                    package_metadata_modified=package_metadata_modified,
                    guid=guid,
                )
                for (
                    package_id,
                    package_name,
                    resource_id,
                    url,
                    org_name,
                    org_id,
                    resource_created,
                    resource_last_modified,
                    resource_metadata_modified,
                    package_metadata_created,
                    package_metadata_modified,
                    guid,
                ) in cur
            ]

    def mark_resource_deleted(self, resource_id: str, package_id: str) -> int:
        assert self._conn is not None, "Repository not entered"
        with self._conn, self._conn.cursor() as cur:
            cur.execute(self.UPDATE_RESOURCE_SQL, {"resource_id": resource_id})
            rowcount = cur.rowcount
            if rowcount > 0:
                cur.execute(self.UPDATE_PACKAGE_MTIME_SQL, {"package_id": package_id})
        return rowcount

    def mark_resource_active(self, resource_id: str, package_id: str) -> int:
        assert self._conn is not None, "Repository not entered"
        with self._conn, self._conn.cursor() as cur:
            cur.execute(self.UPDATE_RESOURCE_ACTIVE_SQL, {"resource_id": resource_id})
            rowcount = cur.rowcount
            if rowcount > 0:
                cur.execute(self.UPDATE_PACKAGE_MTIME_SQL, {"package_id": package_id})
        return rowcount

    def update_resource(self, resource_id: str, package_id: str, action: str) -> int:
        match action:
            case "deleted":
                return self.mark_resource_deleted(resource_id, package_id)
            case "active":
                return self.mark_resource_active(resource_id, package_id)
            case _:
                return 0


def setup_logging(log_path: str) -> logging.Logger:
    logger = logging.getLogger(__name__)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)
    if log_path:
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)
    return logger


def _create_output_filename(filepath, state, timestamp):
    path = Path(filepath)
    return str(path.with_name(f"{path.stem}_{state}_{timestamp}{path.suffix}"))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deletes resources from a check_links CSV report "
        "without fetching from the database or checking link liveness. "
        "Filenames are timestamped templates (module-level constants).",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="check_links CSV report of resources to delete (required)",
    )
    parser.add_argument(
        "--set-state",
        choices=["active", "deleted"],
        required=True,
        help="'action' - updates resources to state == active or deleted",
    )
    parser.add_argument(
        "--mode",
        choices=["dry-run", "live"],
        default="dry-run",
        help="'dry-run' (default) reports only; 'live' marks to-delete resources deleted",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="directory for the reindex list (default: current directory). "
        "Log file is always written to the current directory.",
    )
    parser.add_argument(
        "--local",
        action="store_true",
        default=False,
        help="Logs to file for local runs, otherwise logs to stdout for container runs",
    )
    return parser.parse_args(argv)


def apply(
    *,
    logger: logging.Logger,
    repository: Repository,
    input_path: str,
    reindex_path: str,
    output_report_path: str,
    mode: str,
    set_state: str,
    orgs_to_process: list[str],
) -> None:
    to_reindex: set[str] = set()
    updated = 0
    outfile = None
    writer: csv.DictWriter | None = None

    with contextlib.ExitStack() as stack:
        infile = stack.enter_context(open(input_path, newline="", encoding="utf-8"))
        for row in csv.DictReader(infile):
            if row.get("to-delete", "").lower().strip() != "true" or \
                row.get("org-name", "").strip() not in orgs_to_process:
                continue
            resource_id = row["resource-id"]
            package_id = row["package-id"]
            to_reindex.add(package_id)

            if mode == "live":
                rowcount = repository.update_resource(
                    resource_id, package_id, set_state
                )
                if rowcount > 0:
                    row_copy = row.copy()
                    row_copy["update-applied"] = set_state
                    row_copy["update-applied-on"] = datetime.now(UTC).isoformat(
                        timespec="minutes"
                    )
                    updated += 1
                    # open the report lazily so a run that deletes nothing
                    # doesn't create empty applied file
                    if writer is None:
                        outfile = stack.enter_context(
                            open(output_report_path, "w", newline="", encoding="utf-8")
                        )
                        writer = csv.DictWriter(outfile, fieldnames=list(row_copy))
                        writer.writeheader()
                    writer.writerow(row_copy)
                    outfile.flush()
                else:
                    logger.info(
                        f"skipped {resource_id} (not in correct state to set state to {set_state})"
                    )
            else:
                updated += 1
                logger.info(f"would set state == {set_state} on resource {resource_id}")

    if writer is not None:
        logger.info(f"report of resources set to {set_state}: {output_report_path}")

    with open(reindex_path, "w", encoding="utf-8") as f:
        for package_id in sorted(to_reindex):
            f.write(f"{package_id}\n")

    logger.info(
        f"{set_state} {updated} resources, {len(to_reindex)} packages to reindex"
    )


def get_orgs_to_process() -> str:
    """Get a set of org names from the check_links CSV report."""
    orgs: list[str] = []
    with open("orgs_to_process.txt", encoding="utf-8") as infile:
        for line in infile:
            org_name = line.strip()
            if org_name:
                orgs.append(org_name)
    return orgs


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    log_path = LOG_FILE.format(state=args.set_state) if args.local else None
    reindex_path = os.path.join(
        args.output_dir, REINDEX_FILE.format(state=args.set_state, timestamp=timestamp)
    )

    logger = setup_logging(log_path)
    logger.info(f"mode: {args.mode}")
    logger.info(f"input: {args.input}")
    logger.info(f"set state: {args.set_state}")
    logger.info(f"reindex path: {reindex_path}")

    output_report_path = _create_output_filename(args.input, args.set_state, timestamp)
    logger.info(f"{args.set_state} report path: {output_report_path}")

    dsn = os.environ.get("POSTGRES_URL")
    if not dsn:
        logger.error("POSTGRES_URL env var is not set")
        return 1

    orgs_to_process = get_orgs_to_process()

    with Repository(dsn) as repository:
        apply(
            logger=logger,
            repository=repository,
            input_path=args.input,
            reindex_path=reindex_path,
            output_report_path=output_report_path,
            mode=args.mode,
            set_state=args.set_state,
            orgs_to_process=orgs_to_process
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
