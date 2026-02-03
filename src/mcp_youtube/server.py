"""YouTube MCP Server - backward-compatible @mcp.tool wrappers.

Tool names match the original server.py for drop-in replacement.
"""

from __future__ import annotations

import json

from fastmcp import FastMCP

from .operations import transcripts

mcp = FastMCP("youtube-mcp")


@mcp.tool
def get_transcript(video_url: str, language: str = "en") -> str:
    """Get transcript for a YouTube video.

    Args:
        video_url: YouTube video URL or video ID
        language: Language code (default: 'en'). Examples: 'en', 'es', 'fr', 'de', 'ja'

    Returns:
        Full transcript as plain text
    """
    try:
        return transcripts.get_transcript(video_url, language)
    except Exception as e:
        return f"Error fetching transcript: {e}"


@mcp.tool
def get_transcript_with_timestamps(video_url: str, language: str = "en") -> str:
    """Get transcript with timestamps for a YouTube video.

    Args:
        video_url: YouTube video URL or video ID
        language: Language code (default: 'en')

    Returns:
        Transcript with timestamps in JSON format
    """
    try:
        return transcripts.get_transcript_with_timestamps(video_url, language)
    except Exception as e:
        return f"Error fetching transcript: {e}"


@mcp.tool
def list_available_transcripts(video_url: str) -> str:
    """List all available transcript languages for a video.

    Args:
        video_url: YouTube video URL or video ID

    Returns:
        List of available language codes and names
    """
    try:
        result = transcripts.list_available_transcripts(video_url)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error listing transcripts: {e}"


@mcp.tool
def get_transcript_segment(
    video_url: str, start_time: int, end_time: int, language: str = "en"
) -> str:
    """Get transcript segment between specific timestamps.

    Args:
        video_url: YouTube video URL or video ID
        start_time: Start time in seconds
        end_time: End time in seconds
        language: Language code (default: 'en')

    Returns:
        Transcript segment as plain text
    """
    try:
        return transcripts.get_transcript_segment(video_url, start_time, end_time, language)
    except Exception as e:
        return f"Error fetching transcript segment: {e}"


@mcp.tool
def search_transcript(video_url: str, search_term: str, language: str = "en") -> str:
    """Search for a term in video transcript and return matching segments with timestamps.

    Args:
        video_url: YouTube video URL or video ID
        search_term: Term to search for
        language: Language code (default: 'en')

    Returns:
        Matching segments with timestamps
    """
    try:
        matches = transcripts.search_transcript(video_url, search_term, language)
        if not matches:
            return f"No matches found for '{search_term}'"
        return json.dumps(matches, indent=2)
    except Exception as e:
        return f"Error searching transcript: {e}"


def main():
    """Entry point for MCP stdio server."""
    mcp.run()


if __name__ == "__main__":
    main()
