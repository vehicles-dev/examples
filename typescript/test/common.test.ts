import assert from "node:assert/strict";
import test from "node:test";

import {
  listingFiltersFromVehicle,
  readExampleEnvironment,
  readHistoryReportEnvironment,
  safeVehicleSummary
} from "../src/common.ts";

const completeEnvironment = {
  VEHICLES_API_KEY: "test-api-key",
  VEHICLES_VIN: "TEST-VIN"
};

test("requires the API key and VIN without exposing their values", () => {
  assert.throws(
    () => readExampleEnvironment({ VEHICLES_VIN: "TEST-VIN" }),
    /VEHICLES_API_KEY/u
  );
  assert.throws(
    () => readExampleEnvironment({ VEHICLES_API_KEY: "test-api-key", VEHICLES_VIN: "  " }),
    /VEHICLES_VIN/u
  );
});

test("requires a caller-persisted UUID for a history-report order", () => {
  assert.throws(() => readHistoryReportEnvironment(completeEnvironment), /IDEMPOTENCY_KEY/u);
  assert.throws(
    () =>
      readHistoryReportEnvironment({
        ...completeEnvironment,
        VEHICLES_CONFIRM_BILLABLE_REPORT: "yes",
        VEHICLES_IDEMPOTENCY_KEY: "not-a-uuid"
      }),
    /UUID/u
  );
});

test("requires an exact billable-order confirmation", () => {
  const withKey = {
    ...completeEnvironment,
    VEHICLES_IDEMPOTENCY_KEY: "123e4567-e89b-42d3-a456-426614174000"
  };

  assert.throws(() => readHistoryReportEnvironment(withKey), /CONFIRM_BILLABLE_REPORT=yes/u);
  assert.throws(
    () =>
      readHistoryReportEnvironment({
        ...withKey,
        VEHICLES_CONFIRM_BILLABLE_REPORT: "YES"
      }),
    /CONFIRM_BILLABLE_REPORT=yes/u
  );
});

test("returns validated values only after every guard passes", () => {
  assert.deepEqual(
    readHistoryReportEnvironment({
      ...completeEnvironment,
      VEHICLES_CONFIRM_BILLABLE_REPORT: "yes",
      VEHICLES_IDEMPOTENCY_KEY: "123e4567-e89b-42d3-a456-426614174000"
    }),
    {
      apiKey: "test-api-key",
      idempotencyKey: "123e4567-e89b-42d3-a456-426614174000",
      vin: "TEST-VIN"
    }
  );
});

test("vehicle summaries and listing filters exclude private and extra fields", () => {
  const vehicle = {
    make: "Honda",
    model: "Accord",
    owner: { name: "Private Owner" },
    reportId: "private-report-id",
    trim: "EX",
    vin: "1HGCM82633A004352",
    year: 2003
  };

  assert.deepEqual(safeVehicleSummary(vehicle), {
    make: "Honda",
    model: "Accord",
    trim: "EX",
    year: 2003
  });
  assert.deepEqual(listingFiltersFromVehicle(vehicle), {
    make: "Honda",
    model: "Accord"
  });
});
