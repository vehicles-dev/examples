"""Decode a VIN and print a deliberately limited, privacy-safe summary."""

import json

from vehicles_dev import Vehicles

from common import read_example_environment, run_example, safe_vehicle_summary


def main() -> None:
    environment = read_example_environment()
    with Vehicles(environment["api_key"]) as vehicles:
        decoded = vehicles.decode_vin(environment["vin"])

    print(
        json.dumps(
            {
                "origin": decoded["origin"],
                "vehicle": safe_vehicle_summary(decoded["vehicle"]),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    run_example(main)
