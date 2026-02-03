"""Tests for YouTube transcript operations (pure business logic)."""

from unittest.mock import MagicMock, patch

import pytest

from mcp_youtube.operations.transcripts import (
    extract_video_id,
    get_transcript,
    get_transcript_segment,
    get_transcript_with_timestamps,
    list_available_transcripts,
    search_transcript,
)

# ---------------------------------------------------------------------------
# extract_video_id
# ---------------------------------------------------------------------------


class TestExtractVideoId:
    def test_raw_id(self):
        assert extract_video_id("dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_standard_url(self):
        assert (
            extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            == "dQw4w9WgXcQ"
        )

    def test_short_url(self):
        assert extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_embed_url(self):
        assert (
            extract_video_id("https://www.youtube.com/embed/dQw4w9WgXcQ")
            == "dQw4w9WgXcQ"
        )

    def test_shorts_url(self):
        assert (
            extract_video_id("https://www.youtube.com/shorts/dQw4w9WgXcQ")
            == "dQw4w9WgXcQ"
        )

    def test_url_with_params(self):
        assert (
            extract_video_id(
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=120"
            )
            == "dQw4w9WgXcQ"
        )

    def test_unknown_format_passthrough(self):
        assert extract_video_id("not-a-real-url") == "not-a-real-url"


# ---------------------------------------------------------------------------
# Shared mock helpers
# ---------------------------------------------------------------------------

FAKE_RAW_DATA = [
    {"text": "Hello world", "start": 0.0, "duration": 2.0},
    {"text": "This is a test", "start": 2.0, "duration": 3.0},
    {"text": "Goodbye", "start": 5.0, "duration": 1.5},
]


def _make_mock_transcript(raw_data=None):
    """Create a mock FetchedTranscript with to_raw_data() and iterable Snippet objects."""
    if raw_data is None:
        raw_data = FAKE_RAW_DATA

    mock = MagicMock()
    mock.to_raw_data.return_value = raw_data

    # Build snippet-like objects so TextFormatter can do `line.text`
    snippets = []
    for entry in raw_data:
        s = MagicMock()
        s.text = entry["text"]
        s.start = entry["start"]
        s.duration = entry["duration"]
        snippets.append(s)
    mock.__iter__ = MagicMock(return_value=iter(snippets))

    return mock


def _patch_fetch(raw_data=None):
    """Patch _fetch to return a mock transcript."""
    mock_transcript = _make_mock_transcript(raw_data)
    return patch(
        "mcp_youtube.operations.transcripts._fetch",
        return_value=mock_transcript,
    )


# ---------------------------------------------------------------------------
# get_transcript / get_transcript_with_timestamps
# ---------------------------------------------------------------------------


def test_get_transcript():
    with _patch_fetch():
        result = get_transcript("dQw4w9WgXcQ")
        assert "Hello world" in result
        assert "Goodbye" in result


def test_get_transcript_with_timestamps():
    with _patch_fetch():
        result = get_transcript_with_timestamps("dQw4w9WgXcQ")
        # JSONFormatter calls .to_raw_data() on the FetchedTranscript
        assert "Hello world" in result
        assert "0.0" in result


# ---------------------------------------------------------------------------
# list_available_transcripts
# ---------------------------------------------------------------------------


def test_list_available_transcripts():
    mock_t = MagicMock()
    mock_t.language = "English"
    mock_t.language_code = "en"
    mock_t.is_generated = True
    mock_t.is_translatable = True

    with patch("mcp_youtube.operations.transcripts._api.list", return_value=[mock_t]):
        result = list_available_transcripts("dQw4w9WgXcQ")
        assert len(result) == 1
        assert result[0]["language"] == "English"
        assert result[0]["language_code"] == "en"
        assert result[0]["is_generated"] is True


# ---------------------------------------------------------------------------
# get_transcript_segment
# ---------------------------------------------------------------------------


def test_get_transcript_segment():
    with _patch_fetch():
        result = get_transcript_segment("dQw4w9WgXcQ", 0, 3)
        assert "Hello world" in result
        assert "This is a test" in result
        assert "Goodbye" not in result


def test_get_transcript_segment_empty():
    with _patch_fetch():
        result = get_transcript_segment("dQw4w9WgXcQ", 100, 200)
        assert result == ""


# ---------------------------------------------------------------------------
# search_transcript
# ---------------------------------------------------------------------------


def test_search_transcript_found():
    with _patch_fetch():
        matches = search_transcript("dQw4w9WgXcQ", "hello")
        assert len(matches) == 1
        assert matches[0]["text"] == "Hello world"
        assert matches[0]["timestamp"] == "0:00"


def test_search_transcript_not_found():
    with _patch_fetch():
        matches = search_transcript("dQw4w9WgXcQ", "nonexistent")
        assert matches == []


def test_search_transcript_case_insensitive():
    with _patch_fetch():
        matches = search_transcript("dQw4w9WgXcQ", "HELLO")
        assert len(matches) == 1
