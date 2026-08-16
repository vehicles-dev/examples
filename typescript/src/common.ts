export type Environment = Readonly<Record<string, string | undefined>>;

export interface ExampleEnvironment {
  readonly apiKey: string;
  readonly vin: string;
}

export interface HistoryReportEnvironment extends ExampleEnvironment {
  readonly idempotencyKey: string;
}

export class ExampleConfigurationError extends Error {
  override readonly name = "ExampleConfigurationError";
}

const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/iu;

function requireEnvironment(environment: Environment, name: string): string {
  const value = environment[name]?.trim();
  if (!value) {
    throw new ExampleConfigurationError(`${name} must be set to a nonblank value.`);
  }
  return value;
}

export function readExampleEnvironment(
  environment: Environment = process.env
): ExampleEnvironment {
  return {
    apiKey: requireEnvironment(environment, "VEHICLES_API_KEY"),
    vin: requireEnvironment(environment, "VEHICLES_VIN")
  };
}

export function readHistoryReportEnvironment(
  environment: Environment = process.env
): HistoryReportEnvironment {
  const base = readExampleEnvironment(environment);
  const idempotencyKey = requireEnvironment(environment, "VEHICLES_IDEMPOTENCY_KEY");
  if (!UUID_PATTERN.test(idempotencyKey)) {
    throw new ExampleConfigurationError(
      "VEHICLES_IDEMPOTENCY_KEY must be a caller-generated, persisted UUID."
    );
  }
  if (environment["VEHICLES_CONFIRM_BILLABLE_REPORT"] !== "yes") {
    throw new ExampleConfigurationError(
      "Set VEHICLES_CONFIRM_BILLABLE_REPORT=yes to authorize this billable report order."
    );
  }
  return { ...base, idempotencyKey };
}

function firstString(
  record: Readonly<Record<string, unknown>>,
  names: readonly string[]
): string | undefined {
  for (const name of names) {
    const value = record[name];
    if (typeof value === "string" && value.trim().length > 0) return value;
  }
  return undefined;
}

function firstNumber(
  record: Readonly<Record<string, unknown>>,
  names: readonly string[]
): number | undefined {
  for (const name of names) {
    const value = record[name];
    if (typeof value === "number" && Number.isFinite(value)) return value;
    if (typeof value === "string" && /^\d{4}$/u.test(value)) return Number(value);
  }
  return undefined;
}

export function safeVehicleSummary(
  vehicle: Readonly<Record<string, unknown>>
): Readonly<Record<string, number | string>> {
  const year = firstNumber(vehicle, ["year", "modelYear", "ModelYear"]);
  const make = firstString(vehicle, ["make", "Make"]);
  const model = firstString(vehicle, ["model", "Model"]);
  const trim = firstString(vehicle, ["trim", "Trim"]);
  return {
    ...(year === undefined ? {} : { year }),
    ...(make === undefined ? {} : { make }),
    ...(model === undefined ? {} : { model }),
    ...(trim === undefined ? {} : { trim })
  };
}

export function listingFiltersFromVehicle(
  vehicle: Readonly<Record<string, unknown>>
): Readonly<{ make?: string; model?: string }> {
  const summary = safeVehicleSummary(vehicle);
  return {
    ...(typeof summary["make"] === "string" ? { make: summary["make"] } : {}),
    ...(typeof summary["model"] === "string" ? { model: summary["model"] } : {})
  };
}

export function handleExampleFailure(error: unknown): void {
  if (error instanceof ExampleConfigurationError) {
    console.error(error.message);
  } else {
    console.error("Request failed; no private request or response details were printed.");
  }
  process.exitCode = 1;
}
