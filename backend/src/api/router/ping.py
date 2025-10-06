import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/ping")
@router.get("/health")
def health_check(request: Request) -> JSONResponse:
    if hasattr(request.app.state, "sentence_bert") is False:
        logger.error("Sentence BERT model is not prepared yet")
        raise HTTPException(status_code=400)

    return JSONResponse(content={"ok": "ok"})
