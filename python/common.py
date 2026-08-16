"""Shared environment guards and privacy-safe summary helpers."""

from __future__ import annotations

import os
import re
import sys
from collections.abc import Mapping
from collections.abc import Callable
from typing import TypedDict


class ExampleEnvironment(TypedDict):
    api_key: str
    vin: str


class HistoryReportEnvironment(ExampleEnvironment):
    idempotency_key: str


class ExampleConfigurationError(RuntimeError):
    """Safe-to-print configuration error that never includes environment values."""


_UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def _require_environment(environment: Mapping[str, str], name: str) -> str:
    value = environment.get(name, "").strip()
    if not value:
        raise ExampleConfigurationError(f"{name} must be set to a nonblank value.")
    return value


def read_example_environment(
    environment: Mapping[str, str] | None = None,
) -> ExampleEnvironment:
    values = os.environ if environment is None else environment
    return {
        "api_key": _require_environment(values, "VEHICLES_API_KEY"),
        "vin": _require_environment(values, "VEHICLES_VIN"),
    }


def read_history_report_environment(
    environment: Mapping[str, str] | None = None,
) -> HistoryReportEnvironment:
    values = os.environ if environment is None else environment
    base = read_example_environment(values)
    idempotency_key = _require_environment(values, "VEHICLES_IDEMPOTENCY_KEY")
    if _UUID_PATTERN.fullmatch(idempotency_key) is None:
        raise ExampleConfigurationError(
            "VEHICLES_IDEMPOTENCY_KEY must be a caller-generated, persisted UUID."
        )
    if values.get("VEHICLES_CONFIRM_BILLABLE_REPORT") != "yes":
        raise ExampleConfigurationError(
            "Set VEHICLES_CONFIRM_BILLABLE_REPORT=yes to authorize this billable report order."
        )
    return {**base, "idempotency_key": idempotency_key}


def _first_string(record: Mapping[str, object], names: tuple[str, ...]) -> str | None:
    for name in names:
        value = record.get(name)
        if isinstance(value, str) and value.strip():
            return value
    return None


def _first_year(record: Mapping[str, object], names: tuple[str, ...]) -> int | None:
    for name in names:
        value = record.get(name)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
        if isinstance(value, str) and len(value) == 4 and value.isdecimal():
            return int(value)
    return None


def safe_vehicle_summary(vehicle: Mapping[str, object]) -> dict[str, int | str]:
    """Return only non-sensitive identity fields; VIN is deliberately excluded."""

    candidates: tuple[tuple[str, int | str | None], ...] = (
        ("year", _first_year(vehicle, ("year", "modelYear", "ModelYear"))),
        ("make", _first_string(vehicle, ("make", "Make"))),
        ("model", _first_string(vehicle, ("model", "Model"))),
        ("trim", _first_string(vehicle, ("trim", "Trim"))),
    )
    return {name: value for name, value in candidates if value is not None}


def listing_filters_from_vehicle(vehicle: Mapping[str, object]) -> dict[str, str]:
    summary = safe_vehicle_summary(vehicle)
    return {
        name: value
        for name in ("make", "model")
        if isinstance((value := summary.get(name)), str)
    }


def run_example(main: Callable[[], None]) -> None:
    try:
        main()
    except ExampleConfigurationError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1) from None
    except Exception:
        print(
            "Request failed; no private request or response details were printed.",
            file=sys.stderr,
        )
        raise SystemExit(1) from None
