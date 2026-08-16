import unittest

from common import (
    listing_filters_from_vehicle,
    read_example_environment,
    read_history_report_environment,
    safe_vehicle_summary,
)


COMPLETE_ENVIRONMENT = {
    "VEHICLES_API_KEY": "test-api-key",
    "VEHICLES_VIN": "TEST-VIN",
}


class ExampleEnvironmentTests(unittest.TestCase):
    def test_requires_api_key_and_vin_without_exposing_values(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "VEHICLES_API_KEY"):
            read_example_environment({"VEHICLES_VIN": "TEST-VIN"})

        with self.assertRaisesRegex(RuntimeError, "VEHICLES_VIN"):
            read_example_environment(
                {"VEHICLES_API_KEY": "test-api-key", "VEHICLES_VIN": "  "}
            )

    def test_requires_caller_persisted_uuid_for_history_report(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "IDEMPOTENCY_KEY"):
            read_history_report_environment(COMPLETE_ENVIRONMENT)

        with self.assertRaisesRegex(RuntimeError, "UUID"):
            read_history_report_environment(
                {
                    **COMPLETE_ENVIRONMENT,
                    "VEHICLES_CONFIRM_BILLABLE_REPORT": "yes",
                    "VEHICLES_IDEMPOTENCY_KEY": "not-a-uuid",
                }
            )

    def test_requires_exact_billable_order_confirmation(self) -> None:
        with_key = {
            **COMPLETE_ENVIRONMENT,
            "VEHICLES_IDEMPOTENCY_KEY": "123e4567-e89b-42d3-a456-426614174000",
        }

        with self.assertRaisesRegex(RuntimeError, "CONFIRM_BILLABLE_REPORT=yes"):
            read_history_report_environment(with_key)

        with self.assertRaisesRegex(RuntimeError, "CONFIRM_BILLABLE_REPORT=yes"):
            read_history_report_environment(
                {**with_key, "VEHICLES_CONFIRM_BILLABLE_REPORT": "YES"}
            )

    def test_returns_values_only_after_every_guard_passes(self) -> None:
        self.assertEqual(
            read_history_report_environment(
                {
                    **COMPLETE_ENVIRONMENT,
                    "VEHICLES_CONFIRM_BILLABLE_REPORT": "yes",
                    "VEHICLES_IDEMPOTENCY_KEY": "123e4567-e89b-42d3-a456-426614174000",
                }
            ),
            {
                "api_key": "test-api-key",
                "idempotency_key": "123e4567-e89b-42d3-a456-426614174000",
                "vin": "TEST-VIN",
            },
        )

    def test_vehicle_summaries_and_filters_exclude_private_fields(self) -> None:
        vehicle = {
            "make": "Honda",
            "model": "Accord",
            "owner": {"name": "Private Owner"},
            "reportId": "private-report-id",
            "trim": "EX",
            "vin": "1HGCM82633A004352",
            "year": 2003,
        }

        self.assertEqual(
            safe_vehicle_summary(vehicle),
            {"make": "Honda", "model": "Accord", "trim": "EX", "year": 2003},
        )
        self.assertEqual(
            listing_filters_from_vehicle(vehicle),
            {"make": "Honda", "model": "Accord"},
        )


if __name__ == "__main__":
    unittest.main()
