"""Tests standard tap features using the built-in SDK tests library."""

import json
from pathlib import Path

from singer_sdk.testing import get_tap_test_class

from tap_playstore.tap import TapPlayStore

# CREATE A FILE CALLED `test_config.json`
# USING YOUR GOOGLE CLOUD CREDENTIALS
# IN ORDER TO RUN THE TEST SUITE
with Path(".secrets/test_config.json").open() as f:
    test_config = json.load(f)

# Run standard built-in tap tests from the SDK:
TestTapPlayStore = get_tap_test_class(
    tap_class=TapPlayStore,
    config=test_config,
)
