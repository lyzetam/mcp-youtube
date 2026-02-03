"""YouTube transcript operations - pure business logic.

No auth required. Uses youtube-transcript-api for public video transcripts.
The library uses an instance-based API: YouTubeTranscriptApi().fetch() / .list().
Formatters expect FetchedTranscript objects; raw data ops use .to_raw_data().
"""

from __future__ import annotations

import json
import re
from typing import Any

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter, TextFormatter

# Singleton API instance
_api = YouTubeTranscriptApi()


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from YouTube URL or return ID if already extracted."""
    if len(url_or_id) == 11 and "/" not in url_or_id:
        return url_or_id

    patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)",
        r"youtube\.com\/shorts\/([^&\n?#]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)

    return url_or_id


def _fetch(video_url: str, language: str = "en"):
    """Fetch FetchedTranscript object (pass to formatters or iterate)."""
    video_id = extract_video_id(video_url)
    return _api.fetch(video_id, languages=[language])


def get_transcript(video_url: str, language: str = "en") -> str:
    """Get full transcript as plain text."""
    transcript = _fetch(video_url, language)
    formatter = TextFormatter()
    return formatter.format_transcript(transcript)


def get_transcript_with_timestamps(video_url: str, language: str = "en") -> str:
    """Get transcript with timestamps in JSON format."""
    transcript = _fetch(video_url, language)
    formatter = JSONFormatter()
    return formatter.format_transcript(transcript)


def list_available_transcripts(video_url: str) -> list[dict[str, Any]]:
    """List all available transcript languages for a video."""
    video_id = extract_video_id(video_url)
    transcript_list = _api.list(video_id)

    available = []
    for transcript in transcript_list:
        available.append(
            {
                "language": transcript.language,
                "language_code": transcript.language_code,
                "is_generated": transcript.is_generated,
                "is_translatable": transcript.is_translatable,
            }
        )
    return available


def get_transcript_segment(
    video_url: str, start_time: int, end_time: int, language: str = "en"
) -> str:
    """Get transcript segment between specific timestamps (seconds)."""
    transcript = _fetch(video_url, language)
    raw = transcript.to_raw_data()

    filtered = [
        entry["text"]
        for entry in raw
        if start_time <= entry["start"] <= end_time
    ]
    return " ".join(filtered)


def search_transcript(
    video_url: str, search_term: str, language: str = "en"
) -> list[dict[str, str]]:
    """Search for a term in transcript. Returns matching segments with timestamps."""
    transcript = _fetch(video_url, language)
    raw = transcript.to_raw_data()

    matches = []
    for entry in raw:
        if search_term.lower() in entry["text"].lower():
            timestamp = int(entry["start"])
            minutes = timestamp // 60
            seconds = timestamp % 60
            matches.append(
                {
                    "timestamp": f"{minutes}:{seconds:02d}",
                    "text": entry["text"],
                }
            )
    return matches
