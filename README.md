# tap-playstore

`tap-playstore` is a Singer tap to extract Google Play Store Console Reports.

The following streams can be integrated using this tap:
* stats_by_dimension_buyers_7d
* stats_by_dimension_crashes
* stats_by_dimension_gcm
* stats_by_dimension_installs
* stats_by_dimension_ratings
* stats_by_dimension_ratings_v2
* stats_by_dimension_retained_installers
* stats_overview_crashes
* stats_overview_gcm
* stats_overview_installs
* stats_overview_ratings
* stats_overview_ratings_v2
* reviews
* store_performance_country
* store_performance_traffic_source
* subscriptions_country
* earnings
* play_balance_krw
* sales_reports

_note: the streams prefixed with `stats_by_dimension` consolidate all reports by dimension for the given metric into one common stream._

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.


## Installation

Install from PyPi:

```bash
pipx install tap-playstore
```

Install from GitHub:

```bash
pipx install git+https://github.com/ORG_NAME/tap-playstore.git@main
```

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `batch`

## Configuration

### Accepted Config Options

| Setting                  | Required | Default | Description |
|:-------------------------|:--------:|:-------:|:------------|
| service_account_json_file| False    | None    | Google Cloud Service Account JSON file |
| service_account_json_str | False    | None    | Google Cloud Service Account JSON string |
| start_date               | True     | None    | The earliest record date to sync |
| end_date                 | False    | None    | The most recent record date to sync |
| bucket_name              | True     | None    | The GCS Bucket where Play Console Reports are stored. |
| stream_maps              | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config        | False    | None    | User-defined config values to be used within map expressions. |


A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-playstore --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

<!--
Developer TODO: If your tap requires special access on the source system, or any special authentication requirements, provide those here.
-->

## Usage

You can easily run `tap-playstore` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-playstore --version
tap-playstore --help
tap-playstore --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
poetry run pre-commit install
```

### Create and Run Tests

Tests require a `test_config.json` file to be present. Currently, running tests require an active connection to google cloud.

**TODO:** write proper mocks for google cloud storage.

The `test_config.json` file should mimic the structure of `sample_config.json` file.
```
{
    "start_date": "2024-01-01",
    "bucket_name": "pubsite_prod_rev_00000000000123456789",
    "service_account_json_file": "test_credentials.json"
}
```

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-playstore` CLI interface directly using `poetry run`:

```bash
poetry run tap-playstore --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

<!--
Developer TODO:
Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any "TODO" items listed in
the file.
-->

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-playstore
meltano install
```

Update the meltano config (or populate the environment variables / modify your `.env` file)

```
    config:
      start_date: '2024-01-01T00:00:00Z'
      service_account_json_file: $GOOGLE_PLAY_CREDENTIALS_FILE
      bucket_name: $GOOGLE_PLAY_BUCKET
```


Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-playstore --version
# OR run a test `elt` pipeline:
meltano elt tap-playstore target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
