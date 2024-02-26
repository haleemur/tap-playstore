"""Stream type classes for tap-playstore."""

from __future__ import annotations

import sys

from tap_playstore.client import (
    PlayStoreStreamCsv,
    PlayStoreStreamStatsDimensionCsv,
    PlayStoreStreamZip,
)

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources


SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"
SCHEMAS_DIMENSION_DIR = SCHEMAS_DIR / "stats_by_dimension"
SCHEMAS_OVERVIEW_DIR = SCHEMAS_DIR / "stats_overview"


class StatsByDimensionBuyers7dStream(PlayStoreStreamStatsDimensionCsv):
    """Acquisition Buyers 7 Day Report by Dimension.

    Dimensions are:

    _note: this report has been deprecated_
    """

    report_prefix = "acquisition/buyers_7d/buyers_7d"
    schema_filepath = SCHEMAS_DIMENSION_DIR / "buyers_7d.json"
    name = "stats_by_dimension_buyers_7d"


class StatsByDimensionCrashesStream(PlayStoreStreamStatsDimensionCsv):
    """Crashes Report by Dimension.

    Dimensions are:

    """

    report_prefix = "stats/crashes/crashes"
    schema_filepath = SCHEMAS_DIMENSION_DIR / "crashes.json"
    name = "stats_by_dimension_crashes"


class StatsByDimensionGcmStream(PlayStoreStreamStatsDimensionCsv):
    """GCM Report by Dimension.

    Dimensions are:

    """

    report_prefix = "stats/gcm/gcm"
    schema_filepath = SCHEMAS_DIMENSION_DIR / "gcm.json"
    name = "stats_by_dimension_gcm"


class StatsByDimensionInstallsStream(PlayStoreStreamStatsDimensionCsv):
    """Installs Report by Dimension.

    Dimensions are:

    """

    report_prefix = "stats/installs/installs"
    schema_filepath = SCHEMAS_DIMENSION_DIR / "installs.json"
    name = "stats_by_dimension_installs"


class StatsByDimensionRatingsStream(PlayStoreStreamStatsDimensionCsv):
    """Ratings Report by Dimension.

    Dimensions are:

    """

    report_prefix = "stats/ratings/ratings"
    schema_filepath = SCHEMAS_DIMENSION_DIR / "ratings.json"
    name = "stats_by_dimension_ratings"


class StatsByDimensionRetainedInstallersStream(PlayStoreStreamStatsDimensionCsv):
    """Acquisition Retained Installers Report by Dimension.

    Dimensions are:

    """

    report_prefix = "acquisition/retained_installers/retained_installers"
    schema_filepath = SCHEMAS_DIMENSION_DIR / "retained_installers.json"
    name = "stats_by_dimension_retained_installers"


class StatsOverviewCrashesStream(PlayStoreStreamCsv):
    """Crashes Overview Stats Report."""

    report_prefix = "stats/crashes/crashes"
    schema_filepath = SCHEMAS_OVERVIEW_DIR / "crashes.json"
    name = "stats_overview_crashes"
    report_suffix = "overview.csv"


class StatsOverviewGcmStream(PlayStoreStreamCsv):
    """GCM Overview Stats Report."""

    report_prefix = "stats/gcm/gcm"
    schema_filepath = SCHEMAS_OVERVIEW_DIR / "gcm.json"
    name = "stats_overview_gcm"
    report_suffix = "overview.csv"


class StatsOverviewInstallsStream(PlayStoreStreamCsv):
    """Installs Overview Stats Report."""

    report_prefix = "stats/installs/installs"
    schema_filepath = SCHEMAS_OVERVIEW_DIR / "installs.json"
    name = "stats_overview_installs"
    report_suffix = "overview.csv"


class StatsOverviewRatingsStream(PlayStoreStreamCsv):
    """Ratings Overview Stats Report."""

    report_prefix = "stats/ratings/ratings"
    schema_filepath = SCHEMAS_OVERVIEW_DIR / "ratings.json"
    name = "stats_overview_ratings"
    report_suffix = "overview.csv"


class ReviewsStream(PlayStoreStreamCsv):
    """Reviews."""

    report_prefix = "reviews/reviews"
    schema_filepath = SCHEMAS_DIR / "reviews.json"
    name = "reviews"


class StorePerformanceCountryStream(PlayStoreStreamCsv):
    """Store Performance By Country Report."""

    report_prefix = "stats/store_performance/store_performance"
    schema_filepath = SCHEMAS_DIR / "store_performance_country.json"
    name = "store_performance_country"
    report_suffix = "country.csv"


class StorePerformanceTrafficSourceStream(PlayStoreStreamCsv):
    """Store Performance By Traffic Soruce Report."""

    report_prefix = "stats/store_performance/store_performance"
    schema_filepath = SCHEMAS_DIR / "store_performance_traffic_source.json"
    name = "store_performance_traffic_source"
    report_suffix = "traffic_source.csv"


class SubscriptionsCountryStream(PlayStoreStreamCsv):
    """Subsriptions by Country Report."""

    report_prefix = "financial-stats/subscriptions/subscriptions"
    schema_filepath = SCHEMAS_DIR / "subscriptions_country.json"
    name = "subscriptions_country"
    report_suffix = "country.csv"


class EarningsStream(PlayStoreStreamZip):
    """Earnings Report."""

    report_prefix = "earnings/earnings"
    schema_filepath = SCHEMAS_DIR / "earnings.json"
    name = "earnings"


class PlayBalanceKrwStream(PlayStoreStreamZip):
    """Play Balance KRW Report."""

    report_prefix = "play_balance_krw/play_balance_krw"
    schema_filepath = SCHEMAS_DIR / "play_balance_krw.json"
    name = "play_balance_krw"


class SalesReportStream(PlayStoreStreamZip):
    """Sales Report."""

    report_prefix = "sales/salesreport"
    schema_filepath = SCHEMAS_DIR / "sales_reports.json"
    name = "sales_reports"
