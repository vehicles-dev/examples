import { Vehicles } from "@vehicles-dev/sdk";

import {
  handleExampleFailure,
  listingFiltersFromVehicle,
  readExampleEnvironment
} from "./common.js";

async function main(): Promise<void> {
  const { apiKey, vin } = readExampleEnvironment();
  const vehicles = new Vehicles({ apiKey });

  const decoded = await vehicles.decodeVin(vin);
  const listings = await vehicles.searchListings({
    ...listingFiltersFromVehicle(decoded.vehicle),
    active: true,
    limit: 10,
    validVin: true
  });

  console.log(
    JSON.stringify(
      {
        count: listings.count,
        limit: listings.limit,
        offset: listings.offset,
        total: listings.total
      },
      null,
      2
    )
  );
}

void main().catch(handleExampleFailure);
