import json
import pathlib

from twitter_bookmarks_to_csv.app import bookmarks_to_csv, parse_bookmarks

tests_root = pathlib.Path(__file__).parent


def test_parse_bookmarks_should_return_list():
    sample_file = tests_root / "sample.json"
    sample_parsed = json.loads(sample_file.read_text())
    bookmarks = parse_bookmarks(sample_parsed)
    assert bookmarks[-1].id_str == "1234"


def test_bookmarks_to_csv_should_return_text():
    sample_file = tests_root / "sample.json"
    sample_parsed = json.loads(sample_file.read_text())
    bookmarks = parse_bookmarks(sample_parsed)
    bookmarks_csv = bookmarks_to_csv(bookmarks)
    assert bookmarks_csv.startswith("created_at,id_str,")
