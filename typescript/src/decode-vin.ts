import { Vehicles } from "@vehicles-dev/sdk";

import {
  handleExampleFailure,
  readExampleEnvironment,
  safeVehicleSummary
} from "./common.js";

async function main(): Promise<void> {
  const { apiKey, vin } = readExampleEnvironment();
  const vehicles = new Vehicles({ apiKey });
  const decoded = await vehicles.decodeVin(vin);

  console.log(
    JSON.stringify(
      {
        origin: decoded.origin,
        vehicle: safeVehicleSummary(decoded.vehicle)
      },
      null,
      2
    )
  );
}

void main().catch(handleExampleFailure);
