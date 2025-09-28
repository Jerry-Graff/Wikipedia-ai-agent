import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List
from app.services.wikipedia_services import WikipediaService


# Define response models
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


# Router/Wiki instance
router = APIRouter()
wiki_service = WikipediaService()


@router.get("/search/{query}", response_model=WikipediaSearcResponse)
async def search_wikipedia(query: str):
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
