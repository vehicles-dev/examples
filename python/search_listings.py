"""Search active listings using make/model derived from a private VIN."""

import json

from vehicles_dev import Vehicles

from common import listing_filters_from_vehicle, read_example_environment, run_example


def main() -> None:
    environment = read_example_environment()
    with Vehicles(environment["api_key"]) as vehicles:
        decoded = vehicles.decode_vin(environment["vin"])
        filters = listing_filters_from_vehicle(decoded["vehicle"])
        listings = vehicles.search_listings(
            **filters,
            active=True,
            limit=10,
            valid_vin=True,
        )

    print(
        json.dumps(
            {
                "count": listings["count"],
                "limit": listings["limit"],
                "offset": listings["offset"],
                "total": listings["total"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    run_example(main)
