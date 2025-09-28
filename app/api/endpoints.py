from fastapi import APIRouter

router = APIRouter()


@router.get("/search/{query}")
async def search_wikipedia(query: str):
    # TODO
    return {"message": f"Searching Wikipedia: {query}", query: "query"}
