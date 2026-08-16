import { Vehicles } from "@vehicles-dev/sdk";

import { handleExampleFailure, readHistoryReportEnvironment } from "./common.js";

async function main(): Promise<void> {
  const { apiKey, idempotencyKey, vin } = readHistoryReportEnvironment();
  const vehicles = new Vehicles({ apiKey });

  const order = await vehicles.historyReports.create({ idempotencyKey, vin });
  const result = await vehicles.historyReports.waitForResult(order.id);

  console.log(
    JSON.stringify(
      {
        sections: Object.keys(result.report).sort()
      },
      null,
      2
    )
  );
}

void main().catch(handleExampleFailure);
