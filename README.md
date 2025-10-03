# Wikipedia Research AI Agent

An AI-powered research assistant that conducts comprehensive Wikipedia research using Claude AI. The agent intelligently searches, filters, and synthesizes information from multiple Wikipedia articles to answer complex research questions.

## Why Wikipedia?

AI works best with constraints and reliable data sources. By confining the agent to Wikipedia, we:

- **Reduce hallucinations**: Wikipedia content is regularly edited and fact-checked by real users
- **Enable verification**: Every article used is cited with direct URLs, making it easy to verify information
- **Maintain accuracy**: The structured, encyclopedic nature of Wikipedia provides consistent, factual content
- **Support transparency**: All sources are clearly documented in the output, supporting proper academic citation

## Features

- **Intelligent Query Generation**: Claude AI generates optimized search queries from natural language questions
- **Smart Article Filtering**: AI-powered relevance filtering to find the most pertinent articles
- **Multi-Source Synthesis**: Combines information from multiple Wikipedia articles
- **Automatic Documentation**: Saves research as formatted text files with full source citations
- **RESTful API**: Clean FastAPI endpoints for programmatic access
- **Comprehensive Logging**: Track the research process step-by-step

## Architecture

```
User Query → Claude (Query Planning) → Wikipedia Search → 
Claude (Relevance Filter) → Full Article Retrieval → 
Claude (Synthesis) → Formatted Document Output
```

## Project Structure

```
wikipedia-research-agent/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py          # FastAPI routes
│   └── services/
│       ├── __init__.py
│       ├── claude_service.py     # Claude AI integration
│       ├── wikipedia_service.py  # Wikipedia API wrapper
│       ├── research_agent.py     # Main orchestration logic
│       └── file_service.py       # Document generation
├── research_output/              # Generated research documents
├── .env                          # Environment variables (not in git)
├── .env.example                  # Example environment file
├── .gitignore
├── main.py                       # Application entry point
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

- Python 3.8+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd wikipedia-research-agent
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:

```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
WIKIPEDIA_USER_AGENT_EMAIL=your.email@example.com
```

The email is required by Wikipedia's API terms of service for contact purposes.

## Usage

### Starting the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Interactive API documentation is automatically generated:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

#### 1. Basic Wikipedia Search
**GET** `/search/{query}`

Returns Wikipedia article titles matching the query.

```bash
curl http://localhost:8000/search/artificial%20intelligence
```

#### 2. Detailed Wikipedia Search
**POST** `/search`

Returns article titles with summaries.

```json
{
  "query": "quantum computing",
  "max_results": 5
}
```

#### 3. AI Research Agent (Main Endpoint)
**POST** `/research`

Conducts comprehensive AI-powered research.

```json
{
  "query": "What caused the Irish potato famine and why was 1847 particularly devastating?",
  "num_searches": 3
}
```

**Response includes:**
- Synthesized research document
- List of articles consulted with URLs
- Word counts and statistics
- Local file path to saved document

### Example

```bash
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain the themes and symbolism in Kiyoshi Kurosawa'\''s film Cure",
    "num_searches": 3
  }'
```

The agent will:
1. Generate 3 optimized Wikipedia search queries
2. Search and retrieve article summaries
3. Filter articles by relevance using AI
4. Retrieve full content from relevant articles
5. Synthesize a comprehensive research document
6. Save the document to `research_output/`

## Output Format

Research documents are saved as formatted text files in `research_output/`:

```
research_output/
└── explain-the-themes-and-symbolism-in-cure-20251003-142530.txt
```

Each document includes:
- Formatted headers and sections
- Research question and metadata
- Synthesized content from multiple sources
- Full source citations with URLs
- Generation timestamp and statistics

## Configuration

### Adjusting AI Behavior

In `app/services/claude_service.py`, you can modify:

- **Temperature**: Controls creativity (0.0 = deterministic, 1.0 = creative)
- **Max Tokens**: Response length limit
- **Model**: Claude model version

### Search Parameters

Default parameters can be adjusted in endpoint calls:
- `num_searches`: Number of Wikipedia searches (1-5)
- `max_results`: Results per search (1-20)
- `sentences`: Summary length in sentences

## Known Issues and Future Improvements

### Current Limitations

1. **Prompt Injection Vulnerability**: The agent is susceptible to malicious "ignore previous instructions" style attacks. Users could potentially manipulate the AI to behave unexpectedly.

2. **AI-Generated Writing Style**: The synthesized content tends to sound overly AI-generated:
   - Heavy paraphrasing instead of using article content directly
   - Generic transitional phrases
   - May not pass AI detection tools
   - Could lose some precision from source material

### Planned Improvements

**Security Hardening:**
- Implement prompt injection detection
- Add input sanitization and validation
- Rate limiting on API endpoints
- Content filtering for malicious inputs

**Content Quality:**
- Use more direct quotes and excerpts from articles
- Reduce unnecessary paraphrasing
- Preserve technical terminology and specific details
- Add citation inline with claims
- Implement content authenticity scoring

**Features:**
- PDF export option
- Citation format options (APA, MLA, Chicago)
- Multi-language Wikipedia support
- Batch research queries
- Research history and caching

## Development

### Running Tests

```bash
pytest
```

### Code Style

This project follows PEP 8 guidelines. Format code with:

```bash
black .
flake8
```

## Dependencies

Key dependencies:
- `fastapi`: Web framework
- `anthropic`: Claude AI integration
- `wikipedia`: Wikipedia API wrapper
- `pydantic`: Data validation
- `uvicorn`: ASGI server
- `python-dotenv`: Environment management

See `requirements.txt` for complete list with versions.

## API Rate Limits

- **Wikipedia**: Generally permissive, but respect their terms of service
- **Anthropic Claude**: Depends on your API tier
  - Monitor usage in Anthropic Console
  - Each research query uses ~2-4 API calls

## Contributing

Contributions welcome! Areas needing work:
1. Security improvements (prompt injection protection)
2. Content quality enhancements
3. Additional output formats
4. Test coverage
5. Error handling improvements

## License

[Your License Here]

## Acknowledgments

- Wikipedia for providing free, comprehensive knowledge
- Anthropic for Claude AI API
- FastAPI for the excellent web framework

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review API logs for debugging

---

**Note**: This is an educational project demonstrating AI agent architecture and API integration. Always verify important information from original Wikipedia sources provided in citations.