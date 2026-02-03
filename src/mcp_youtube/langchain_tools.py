"""LangChain @tool wrappers for YouTube transcript operations.

Usage:
    from mcp_youtube.langchain_tools import TOOLS

    # Or import individual tools:
    from mcp_youtube.langchain_tools import yt_get_transcript, yt_search_transcript
"""

from __future__ import annotations

import json
from typing import Optional

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from .operations import transcripts


# =============================================================================
# Get Transcript
# =============================================================================


class GetTranscriptInput(BaseModel):
    video_url: str = Field(description="YouTube video URL or video ID")
    language: str = Field(default="en", description="Language code (e.g. 'en', 'es', 'fr')")


@tool(args_schema=GetTranscriptInput)
def yt_get_transcript(video_url: str, language: str = "en") -> str:
    """Get full transcript for a YouTube video as plain text."""
    try:
        return transcripts.get_transcript(video_url, language)
    except Exception as e:
        return f"Error fetching transcript: {e}"


# =============================================================================
# Get Transcript with Timestamps
# =============================================================================


@tool(args_schema=GetTranscriptInput)
def yt_get_transcript_with_timestamps(video_url: str, language: str = "en") -> str:
    """Get transcript with timestamps for a YouTube video in JSON format."""
    try:
        return transcripts.get_transcript_with_timestamps(video_url, language)
    except Exception as e:
        return f"Error fetching transcript: {e}"


# =============================================================================
# List Available Transcripts
# =============================================================================


class ListTranscriptsInput(BaseModel):
    video_url: str = Field(description="YouTube video URL or video ID")


@tool(args_schema=ListTranscriptsInput)
def yt_list_available_transcripts(video_url: str) -> str:
    """List all available transcript languages for a YouTube video."""
    try:
        result = transcripts.list_available_transcripts(video_url)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error listing transcripts: {e}"


# =============================================================================
# Get Transcript Segment
# =============================================================================


class GetSegmentInput(BaseModel):
    video_url: str = Field(description="YouTube video URL or video ID")
    start_time: int = Field(description="Start time in seconds")
    end_time: int = Field(description="End time in seconds")
    language: str = Field(default="en", description="Language code (e.g. 'en', 'es')")


@tool(args_schema=GetSegmentInput)
def yt_get_transcript_segment(
    video_url: str, start_time: int, end_time: int, language: str = "en"
) -> str:
    """Get transcript segment between specific timestamps (in seconds)."""
    try:
        return transcripts.get_transcript_segment(video_url, start_time, end_time, language)
    except Exception as e:
        return f"Error fetching transcript segment: {e}"


# =============================================================================
# Search Transcript
# =============================================================================


class SearchTranscriptInput(BaseModel):
    video_url: str = Field(description="YouTube video URL or video ID")
    search_term: str = Field(description="Term to search for in the transcript")
    language: str = Field(default="en", description="Language code (e.g. 'en', 'es')")


@tool(args_schema=SearchTranscriptInput)
def yt_search_transcript(
    video_url: str, search_term: str, language: str = "en"
) -> str:
    """Search for a term in a YouTube video transcript. Returns matching segments with timestamps."""
    try:
        matches = transcripts.search_transcript(video_url, search_term, language)
        if not matches:
            return f"No matches found for '{search_term}'"
        return json.dumps(matches, indent=2)
    except Exception as e:
        return f"Error searching transcript: {e}"


# =============================================================================
# Exported tool list
# =============================================================================

TOOLS = [
    yt_get_transcript,
    yt_get_transcript_with_timestamps,
    yt_list_available_transcripts,
    yt_get_transcript_segment,
    yt_search_transcript,
]
