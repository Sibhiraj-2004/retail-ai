from fastapi import APIRouter
from app.schemas.request import QueryRequest
from app.schemas.response import QueryResponse
from app.services.query_service import process_query

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    result = ""
    try:
        result = process_query(request.query, session_id="default")
    except Exception as e:
        print(e)
        return QueryResponse(response="processing query failed")
    if len(result) == 0:
        return QueryResponse(response="Please add more details about the query")
    return QueryResponse(response=result)
