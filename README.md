# mcp-youtube

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

YouTube transcript operations as a Python library, LangChain tools, and MCP server. Fetch transcripts, search within them, extract segments by timestamp, and list available languages -- all without a YouTube API key.

## Features

**5 tools:**

- **get_transcript** -- get full transcript as plain text
- **get_transcript_with_timestamps** -- get transcript with timestamps in JSON format
- **list_available_transcripts** -- list available transcript languages for a video
- **get_transcript_segment** -- extract transcript between specific timestamps
- **search_transcript** -- search for a term and get matching segments with timestamps

No API key required -- uses `youtube-transcript-api` to fetch publicly available transcripts.

## Installation

```bash
# Core library only
pip install .

# With MCP server
pip install ".[mcp]"

# With LangChain tools
pip install ".[langchain]"

# Everything
pip install ".[all]"
```

## Configuration

No configuration needed. This package works out of the box for public YouTube videos.

## Quick Start

### MCP Server

```bash
mcp-youtube
```

### LangChain Tools

```python
from mcp_youtube.langchain_tools import TOOLS, yt_get_transcript, yt_search_transcript

# Get a video transcript
result = yt_get_transcript.invoke({
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
})

# Search within a transcript
result = yt_search_transcript.invoke({
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "search_term": "never gonna"
})

# Or pass all tools to an agent
from langchain.agents import AgentExecutor
agent = AgentExecutor(tools=TOOLS, ...)
```

### Python Library

```python
from mcp_youtube.operations.transcripts import get_transcript, search_transcript

text = get_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
matches = search_transcript("dQw4w9WgXcQ", "never gonna")
```

## License

MIT
