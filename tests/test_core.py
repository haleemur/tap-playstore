"""Tests standard tap features using the built-in SDK tests library."""
from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from singer_sdk.testing import get_tap_test_class

import tap_playstore.streams as s
from tap_playstore.tap import TapPlayStore

if TYPE_CHECKING:
    from tap_playstore.client import PlayStoreStream

# CREATE A FILE CALLED `test_config.json`
# USING YOUR GOOGLE CLOUD CREDENTIALS
# IN ORDER TO RUN THE TEST SUITE
with Path(".secrets/test_config.json").open() as f:
    test_config = json.load(f)


class MinimalTapPlayStore(TapPlayStore):
    """Minial Tap with only one stream for fast testing."""

    def discover_streams(self) -> list[PlayStoreStream]:
        """Minimal discover of just 1 stream."""
        return [
            s.StatsOverviewInstallsStream(self),
        ]


TestMinimalPlayStore = get_tap_test_class(
    tap_class=MinimalTapPlayStore, config=test_config
)

# Run standard built-in tap tests from the SDK:
TestTapPlayStore = get_tap_test_class(
    tap_class=TapPlayStore,
    config=test_config,
)
