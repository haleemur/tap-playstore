"""Custom client handling, including `PlayStoreStreamBase` class."""

from __future__ import annotations

import csv
import json
import re
from functools import cached_property
from io import TextIOWrapper
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable
from zipfile import ZipFile

from google.cloud.storage import Blob, Bucket, Client
from singer_sdk.streams.core import REPLICATION_INCREMENTAL, Stream

if TYPE_CHECKING:
    from datetime import datetime


class PlayStoreStream(Stream):
    """Base Class to interact with Google Play Store Console Reports.

    Child classes must override the following methods
    or declare the following attributes:
    * report_prefix
    * suffix_matches
    * yield_records_from_file
    * schema_filepath
    * name
    _Note that a custom `suffix_matches` may require defining `report_suffix` as well._
    """

    replication_method = REPLICATION_INCREMENTAL
    replication_key = "_file_updated_at"

    def _yield_rows_from_file(
        self,
        reader: Iterable,
        header: list[str],
        static_fields: dict[str, str | int | datetime],
    ) -> Iterable[dict]:
        """Yield processed rows from csv file as dict."""
        fields = [re.sub(r"(\W|\s)+", "_", fn.lower()).rstrip("_") for fn in header]
        for i, row in enumerate(reader):
            context = {
                "fields": set(fields),
                "static_fields": static_fields,
                "_file_lineno": i,
            }
            rec = self.convert_types_and_add_metadata(dict(zip(fields, row)), context)
            yield rec

    def convert_types_and_add_metadata(
        self, row: dict[str, Any], context: dict
    ) -> dict[str, Any]:
        """Post process string values read from the CSV files."""
        fields = context["fields"]
        static_fields = context["static_fields"]
        file_lineno = {"_file_lineno": context["_file_lineno"]}
        typemap = {f: t for f, t in self._typemap_from_string.items() if f in fields}
        for field, type_ in typemap.items():
            if type_ == "integer":
                row[field] = int(row[field])
            elif type_ == "null-integer":
                row[field] = None if row[field] == "" else int(row[field])
            elif type_ == "number":
                row[field] = float(row["field"])
            elif type_ == "null-number":
                row[field] = None if row[field] == "" else float(row[field])
            elif type_ in {"string", "null-string"}:
                continue
            else:
                raise NotImplementedError
        return row | static_fields | file_lineno

    @property
    def _typemap_from_string(self) -> dict[str, str]:
        """Provide proper types in order to conform to the message schema."""
        tmap = {}
        for field, kind in self.schema["properties"].items():
            if isinstance(kind["type"], str):
                tmap[field] = kind["type"]
            elif isinstance(kind["type"], list) and "null" in kind["type"]:
                tmap[field] = "null-" + "-".join(set(kind["type"]) - {"null"})
        return tmap

    @cached_property
    def gcs_client(self) -> Bucket:
        """Return teh gcs client's bucket interface."""
        if "service_account_json_str" in self.config:
            auth_info = json.loads(self._config["service_account_json_str"])
        else:
            with Path(self.config["service_account_json_file"]).open() as f:
                auth_info = json.load(f)

        client = Client.from_service_account_info(auth_info)
        return client.bucket(self._config["bucket_name"])

    def yield_records_from_file(
        self, fname: Path, static_fields: dict
    ) -> Iterable[dict]:
        """Yield Records from downloaded file. Child class must implement."""
        raise NotImplementedError

    @property
    def report_prefix(self) -> str:
        """Prefix to filter the report with. Child class must implement it."""
        raise NotImplementedError

    @property
    def report_suffix(self) -> str | None:
        """Suffix to filter the report with."""
        return None

    def suffix_matches(self, obj: Blob) -> bool:
        """Return True if blob's suffix is as expected."""
        raise NotImplementedError

    def get_records(
        self,
        context: dict | None,
    ) -> Iterable[dict]:
        """Return a generator of record-type dictionary objects.

        Args:
            context: Stream partition or context dictionary.
        """
        start_at = self.get_starting_timestamp(context)
        for obj in self.gcs_client.list_blobs(prefix=self.report_prefix):
            if obj.updated > start_at and self.suffix_matches(obj):
                try:
                    fname = Path(obj.name.split("/")[-1])
                    tstamp = obj.updated.isoformat(timespec="milliseconds")
                    obj.download_to_filename(fname)
                    static_fields = {
                        "_file_updated_at": tstamp,
                        "_file_path": obj.name,
                        "_bucket": obj.bucket.name,
                    }
                    yield from self.yield_records_from_file(fname, static_fields)
                finally:
                    if self.clean_up_downloads:
                        fname.unlink()

    @property
    def clean_up_downloads(self) -> bool:
        """Flag controls if downloaded files are automatically deleted after use.

        It is useful in testing settings to set this to `False`
        """
        return True


class PlayStoreStreamZip(PlayStoreStream):
    """Fetch Zipped CSV Google Play Store Reports from google cloud storage.

    Child Classes must override:
    * report_prefix
    * schema_filepath
    * name
    """

    @property
    def encoding(self) -> str:
        """Return the file encoding."""
        return "utf-8"

    @property
    def report_suffix(self) -> str:
        """Suffix to filter the report with."""
        return ".zip"

    def yield_records_from_file(
        self, fname: Path, static_fields: dict
    ) -> Iterable[dict]:
        """Open downloaded zipfile and yield transformed records.

        note: The downloaded zipfiles typically have 1 utf-8 encoded csv.
        """
        with ZipFile(fname) as zip_:
            for name in zip_.namelist():
                with zip_.open(name) as f:
                    reader = csv.reader(TextIOWrapper(f, self.encoding))
                    header = next(reader)
                    yield from self._yield_rows_from_file(
                        reader=reader, header=header, static_fields=static_fields
                    )

    def suffix_matches(self, obj: Blob) -> bool:
        """Return True if blob's suffix is as expected."""
        return obj.name.endswith(self.report_suffix)


class PlayStoreStreamCsv(PlayStoreStream):
    """Fetch CSV Google Play Store Reports from google cloud storage.

    Child Classes must override:
    * report_prefix
    * schema_filepath
    * name

    Optionally, the child class may override the property `encoding` if needed
    (default encoding `utf-16-le`), and `report_suffix` if a more specific filter
    is required.
    """

    @property
    def encoding(self) -> str:
        """Return the file encoding."""
        return "utf-16-le"

    @property
    def report_suffix(self) -> str:
        """Suffix to filter the report with."""
        return ".csv"

    def yield_records_from_file(
        self, fname: Path, static_fields: dict
    ) -> Iterable[dict]:
        """Open downloaded file and yield transformed records."""
        with fname.open(encoding=self.encoding) as f:
            f.read(1)  # skip the BOM Mark
            reader = csv.reader(f)
            header = next(reader)
            yield from self._yield_rows_from_file(
                reader=reader, header=header, static_fields=static_fields
            )

    def suffix_matches(self, obj: Blob) -> bool:
        """Return True if blob's suffix is as expected."""
        return obj.name.endswith(self.report_suffix)


class PlayStoreStreamStatsDimensionCsv(PlayStoreStream):
    """Fetches all dimensional summary stats reports from Google Play Store Console.

    Child Classes must override:
    * report_prefix
    * schema_filepath
    * name

    Optionally, the child class may override the property `encoding` if needed
    (default encoding `utf-16-le`)
    """

    @property
    def encoding(self) -> str:
        """Return the file encoding."""
        return "utf-16-le"

    @property
    def dimensions(self) -> dict[str, str]:
        """Map file suffixes used for stats reports to dimension column names."""
        return {
            "app_version.csv": "App Version Code",
            "carrier.csv": "Carrier",
            "channel.csv": "Acquisition Channel",
            "country.csv": "Country",
            "device.csv": "Device",
            "google.csv": "Keyword",
            "language.csv": "Language",
            "message_status.csv": "GCM Message Status",
            "os_version.csv": "Android OS Version",
            "play_country.csv": "Country (Play Store)",
            "response_code.csv": "GCM Response Code",
            "tablets.csv": "Tablets",
            "utm_tagged.csv": "UTM source/campaign",
        }

    def get_dimension_name(self, fname: Path | str) -> str | None:
        """Return the column name used as dimension."""
        for dim, colname in self.dimensions.items():
            if str(fname).endswith(dim):
                return colname
        return None

    def suffix_matches(self, obj: Blob) -> bool:
        """Return True if blob's suffix is as expected."""
        return self.get_dimension_name(obj.name) is not None

    def yield_records_from_file(
        self, fname: Path, static_fields: dict
    ) -> Iterable[dict]:
        """Open downloaded file and yield transformed records."""
        dimension_name = self.get_dimension_name(fname)
        static_fields_ = static_fields.copy()
        static_fields_["dimension_name"] = dimension_name
        with fname.open(encoding=self.encoding) as f:
            f.read(1)  # skip the BOM Mark
            reader = csv.reader(f)
            header = next(reader)
            header_replaced = [
                "dimension_value" if fn == dimension_name else fn for fn in header
            ]
            yield from self._yield_rows_from_file(
                reader=reader, header=header_replaced, static_fields=static_fields_
            )
