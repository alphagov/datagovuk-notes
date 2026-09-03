import argparse
from datetime import UTC, datetime
import json
import os
import logging
import psycopg2
import pysolr
import sys


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


def get_org_list(org_list_path):
    org_list = []
    with open(org_list_path, "r") as f:
        for line in f:
            org_name = line.strip()
            if org_name:
                org_list.append(org_name)
    return org_list


def has_org_resources(org_name):
    with psycopg2.connect(os.getenv("CKAN_SQLALCHEMY_URL")) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'SELECT id FROM "group" WHERE name = \'{org_name}\'')
            org_id = cursor.fetchone()
            if org_id:
                cursor.execute(f"SELECT COUNT(*) FROM resource WHERE state = 'active' AND package_id IN "
                            f"(SELECT id FROM package WHERE state = 'active' AND owner_org = '{org_id[0]}');")
                count = cursor.fetchone()
                return count[0] > 0
            else:
                raise ValueError(f"Organisation {org_name} not found in the database.")


def _delete_from_database(org_name):
    conn = None
    with psycopg2.connect(os.getenv("CKAN_SQLALCHEMY_URL")) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'UPDATE "group_extra_revision" SET state = \'deleted\' WHERE group_id IN (SELECT id FROM "group" WHERE name = \'{org_name}\')')
            cursor.execute(f'UPDATE "group_extra" SET state = \'deleted\' WHERE group_id IN (SELECT id FROM "group" WHERE name = \'{org_name}\')')
            cursor.execute(f'UPDATE "group_revision" SET state = \'deleted\' WHERE name = \'{org_name}\'')
            cursor.execute(f'UPDATE "group" SET state = \'deleted\' WHERE name = \'{org_name}\'')


def _delete_from_solr(org_name):
    solr_url = os.getenv("CKAN_SOLR_URL")
    solr = pysolr.Solr(solr_url, always_commit=True)
    datasets = solr.search(f'site_id:dgu_organisations_2 AND name:"{org_name}"')

    if datasets.hits > 0:
        solr.delete(q=f'site_id:dgu_organisations_2 AND name:"{org_name}"')
    else:
        raise ValueError(f"Organisation {org_name} not found in Solr.")


def delete_orgs(logger, org_list, report_only=True):
    errors = []
    num_deleted_from_database = 0
    num_deleted_from_solr = 0

    for i, org in enumerate(org_list):
        deleted = False
        try:
            if has_org_resources(org):
                logger.info(f"Organisation {org} has resources, skipping...")
            else:
                logger.info(f"Organisation {org} has no resources, deleting...")

                try:
                    if not report_only:
                        _delete_from_database(org)

                    num_deleted_from_database += 1
                except Exception as exc:
                    errors.append((org, "Error deleting org from database:" + str(exc)))

                try:
                    if not report_only:
                        _delete_from_solr(org)

                    num_deleted_from_solr += 1
                except Exception as exc:
                    errors.append((org, "Error deleting org from solr:" + str(exc)))
                deleted = True

            logger.info(f"{i + 1}/{len(org_list)}: {('Will delete' if report_only else 'deleted') if deleted else 'Skipped'} {org}")
        except Exception as exc:
            errors.append((org, "Error checking org resources: " + str(exc)))
    
    return errors, num_deleted_from_database, num_deleted_from_solr


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--orgs-path",
        "-o",
        default="",
        help="Organisation list to delete (Required)",
    )
    parser.add_argument(
        "--log-dir",
        "-l",
        default=".",
        help="Log file report for organisations deleted",
    )
    parser.add_argument(
        "--report-only",
        "-r",
        default="True",
        help="Report only (default True)",
    )

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M")
    log_path = os.path.join(args.log_dir, f"delete_orgs_{timestamp}.log")
    logger = setup_logging(log_path)
    logger.info("===== settings =====")
    logger.info(f"Organisation list path: {args.orgs_path}")
    logger.info(f"Report only: {args.report_only}")
    logger.info(f"Log path: {log_path}")
    logger.info("====================")

    if not args.orgs_path:
        logger.error(
            "Organisation list not defined, use -o <org> or --org <org> to pass it in"
        )
        return 1

    try:
        org_list = get_org_list(args.orgs_path)
        errors, num_deleted_from_database, num_deleted_from_solr = delete_orgs(logger, org_list, report_only=args.report_only == "True")
        for org, error in errors:
            logger.error(f"Error deleting {org}: {error}")

        logger.info(f"{('Will delete' if args.report_only == 'True' else 'deleted')} {num_deleted_from_database} organisations from database")
        logger.info(f"{('Will delete' if args.report_only == 'True' else 'deleted')} {num_deleted_from_solr} organisations from solr")
        print(f"Logs written to {log_path}")
    except Exception as e:
        logger.error(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())
