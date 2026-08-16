"""Order one billable durable history report, wait, and print section names."""

import json

from vehicles_dev import Vehicles

from common import read_history_report_environment, run_example


def main() -> None:
    environment = read_history_report_environment()
    with Vehicles(environment["api_key"]) as vehicles:
        order = vehicles.history_reports.create(
            environment["vin"],
            idempotency_key=environment["idempotency_key"],
        )
        result = vehicles.history_reports.wait_for_result(order["id"])

    print(json.dumps({"sections": sorted(result["report"])}, indent=2))


if __name__ == "__main__":
    run_example(main)
