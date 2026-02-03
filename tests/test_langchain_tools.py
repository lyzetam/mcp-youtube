"""Tests for YouTube LangChain tool wrappers."""

from unittest.mock import patch

from mcp_youtube.langchain_tools import (
    TOOLS,
    yt_get_transcript,
    yt_get_transcript_with_timestamps,
    yt_list_available_transcripts,
    yt_get_transcript_segment,
    yt_search_transcript,
)


class TestToolRegistration:
    """Verify all tools are properly registered and have correct metadata."""

    def test_tools_list_length(self):
        assert len(TOOLS) == 5

    def test_all_tools_have_yt_prefix(self):
        for t in TOOLS:
            assert t.name.startswith("yt_"), f"{t.name} missing yt_ prefix"

    def test_all_tools_have_descriptions(self):
        for t in TOOLS:
            assert t.description, f"{t.name} missing description"

    def test_all_tools_have_invoke(self):
        for t in TOOLS:
            assert hasattr(t, "invoke"), f"{t.name} missing invoke method"

    def test_tool_names(self):
        names = {t.name for t in TOOLS}
        expected = {
            "yt_get_transcript",
            "yt_get_transcript_with_timestamps",
            "yt_list_available_transcripts",
            "yt_get_transcript_segment",
            "yt_search_transcript",
        }
        assert names == expected


class TestToolInvocation:
    """Verify tools correctly delegate to operations layer."""

    @patch("mcp_youtube.langchain_tools.transcripts.get_transcript")
    def test_get_transcript(self, mock_op):
        mock_op.return_value = "Hello world"
        result = yt_get_transcript.invoke({"video_url": "abc123", "language": "en"})
        assert result == "Hello world"
        mock_op.assert_called_once_with("abc123", "en")

    @patch("mcp_youtube.langchain_tools.transcripts.get_transcript_with_timestamps")
    def test_get_transcript_with_timestamps(self, mock_op):
        mock_op.return_value = '[{"text": "Hi"}]'
        result = yt_get_transcript_with_timestamps.invoke(
            {"video_url": "abc123", "language": "en"}
        )
        assert "Hi" in result

    @patch("mcp_youtube.langchain_tools.transcripts.list_available_transcripts")
    def test_list_available_transcripts(self, mock_op):
        mock_op.return_value = [{"language": "English", "language_code": "en"}]
        result = yt_list_available_transcripts.invoke({"video_url": "abc123"})
        assert "English" in result

    @patch("mcp_youtube.langchain_tools.transcripts.get_transcript_segment")
    def test_get_transcript_segment(self, mock_op):
        mock_op.return_value = "segment text"
        result = yt_get_transcript_segment.invoke(
            {"video_url": "abc123", "start_time": 0, "end_time": 10, "language": "en"}
        )
        assert result == "segment text"

    @patch("mcp_youtube.langchain_tools.transcripts.search_transcript")
    def test_search_transcript_found(self, mock_op):
        mock_op.return_value = [{"timestamp": "0:05", "text": "match"}]
        result = yt_search_transcript.invoke(
            {"video_url": "abc123", "search_term": "match", "language": "en"}
        )
        assert "match" in result

    @patch("mcp_youtube.langchain_tools.transcripts.search_transcript")
    def test_search_transcript_not_found(self, mock_op):
        mock_op.return_value = []
        result = yt_search_transcript.invoke(
            {"video_url": "abc123", "search_term": "nope", "language": "en"}
        )
        assert "No matches found" in result

    @patch("mcp_youtube.langchain_tools.transcripts.get_transcript")
    def test_error_handling(self, mock_op):
        mock_op.side_effect = RuntimeError("API down")
        result = yt_get_transcript.invoke({"video_url": "abc123", "language": "en"})
        assert "Error" in result
