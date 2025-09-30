import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List
from app.services.wikipedia_services import WikipediaService
from app.services.research_agent import ResearchAgent


# Respone Models /search - just wiki api no claude
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=100, description="Search query")
    max_results: int = Field(default=5, ge=1, le=20, description="Maximum resuts (1-20)")

    @field_validator('query')
    def query_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Query cannot be empty or whitespace.")
        return v.strip()


class WikipediaPage(BaseModel):
    title: str
    summary: str = Field(..., description="Page summary")
    url: str = Field(..., description="Wikipedia URL")
    word_count: int = Field(..., ge=0, description="Number of word in summary")


class DetailedSearchResponse(BaseModel):
    query: str
    total_found: int
    pages: List[WikipediaPage]
    search_time: float = Field(..., description="Search time in seconds")


class WikipediaSearcResponse(BaseModel):
    message: str
    query: str
    titles: List[str]


# Response Models /research - claude api
class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=5, max_length=200, description="Research Questions")
    num_searches: int = Field(default=3, ge=1, le=5, description="Number of Wiki searches: 1-5")

    @field_validator('query')
    def query_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Query cannot be empty or whitespace.")
        return v.strip()


class ArticleData(BaseModel):
    title: str
    url: str
    word_count: int
    content_preview: str = Field(..., description="First 500 chars of article")


class ResearchResponse(BaseModel):
    user_query: str
    search_queries: List[str]
    total_articles: int
    total_words: int
    candidates_considered: int
    articles: List[ArticleData]


# Initalize Services
router = APIRouter()
wiki_service = WikipediaService()
research_agent = ResearchAgent()

@router.get("/search/{query}", response_model=WikipediaSearcResponse)
async def search_wikipedia(query: str):
    """Basic Search - Returns: titles"""
    try:
        results = wiki_service.search_titles(query)

        # Return data matching model
        return WikipediaSearcResponse(
            message=f"Found {len(results)} results for {query}",
            query=query,
            titles=results
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=DetailedSearchResponse)
async def advanced_search(request: SearchRequest):
    "Detailed Search - Returns: titles + summaries"
    start_time = time.time()

    try:
        results = wiki_service.search_titles(request.query, request.max_results)

        # Get detailed info for each page
        pages = []
        for title in results:
            summary = wiki_service.get_page_summary(title)
            if summary:
                pages.append(WikipediaPage(
                    title=title,
                    summary=summary,
                    url=f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                    word_count=len(summary.split())
                ))

        search_time = round((time.time() - start_time), 2)

        return DetailedSearchResponse(
            query=request.query,
            total_found=len(pages),
            pages=pages,
            search_time=search_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/research", response_model=ResearchResponse)
async def conduct_ai_research(request: ResearchRequest):
    """
    AI-powered research endpoint that:
    1. Uses Claude to generate smart search queries
    2. Searches Wikipedia multiple times
    3. Filters articles by relevance using AI
    4. Retrieves full content only for relevant articles

    Main AI agent endpoint!
    """

    try:
        results = research_agent.conduct_research(
            user_query=request.query,
            num_searches=request.num_searches
        )

        # Format articles for response (preview only)
        articles_formatted = [
            ArticleData(
                title=article['title'],
                url=article['url'],
                word_count=article['word_count'],
                content_preview=article['content'][:500] + "..."
            )
            for article in results['articles']
        ]

        return ResearchResponse(
            user_query=results['user_query'],
            search_queries=results['search_queries'],
            total_articles=results['total_articles'],
            total_words=results['total_words'],
            candidates_considered=results['candidates_considered'],
            articles=articles_formatted
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")
