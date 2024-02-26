"""PlayStore tap class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_playstore import streams

if TYPE_CHECKING:
    from tap_playstore.client import PlayStoreStream


class TapPlayStore(Tap):
    """PlayStore tap class."""

    name = "tap-playstore"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "service_account_json_file",
            th.StringType,
            required=False,
            secret=False,  # Flag config as protected.
            description="Google Cloud Service Account JSON file",
        ),
        th.Property(
            "service_account_json_str",
            th.ArrayType(th.StringType),
            required=False,
            secret=True,
            description="Google Cloud Service Account JSON string",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            required=True,
            secret=False,
            description="The earliest record date to sync",
        ),
        th.Property(
            "end_date",
            th.DateTimeType,
            required=False,
            secret=False,
            description="The most recent record date to sync",
        ),
        th.Property(
            "bucket_name",
            th.StringType,
            required=True,
            secret=False,
            description="The GCS Bucket where Play Console Reports are stored.",
        ),
    ).to_dict()

    def discover_streams(self) -> list[PlayStoreStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.StatsByDimensionBuyers7dStream(self),
            streams.StatsByDimensionCrashesStream(self),
            streams.StatsByDimensionGcmStream(self),
            streams.StatsByDimensionInstallsStream(self),
            streams.StatsByDimensionRatingsStream(self),
            streams.StatsByDimensionRetainedInstallersStream(self),
            streams.StatsOverviewCrashesStream(self),
            streams.StatsOverviewGcmStream(self),
            streams.StatsOverviewInstallsStream(self),
            streams.StatsOverviewRatingsStream(self),
            streams.ReviewsStream(self),
            streams.StorePerformanceCountryStream(self),
            streams.StorePerformanceTrafficSourceStream(self),
            streams.SubscriptionsCountryStream(self),
            streams.EarningsStream(self),
            streams.PlayBalanceKrwStream(self),
            streams.SalesReportStream(self),
        ]


if __name__ == "__main__":
    TapPlayStore.cli()
