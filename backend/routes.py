from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from backend.ai_core.gemini_generator import GeminiDocumentGenerator
from backend.config import MAX_DOCUMENT_CHARS
router=APIRouter(); generator=GeminiDocumentGenerator()
class DocumentRequest(BaseModel):
    document_type:str=Field(...,min_length=2,max_length=100)
    parties:str=Field(...,min_length=2,max_length=5000)
    terms:list[str]=Field(default_factory=list,max_length=50)
    effective_date:str=Field(...,min_length=2,max_length=100)
    @field_validator("document_type","parties","effective_date")
    @classmethod
    def strip_text(cls,v):
        v=v.strip()
        if not v: raise ValueError("This field cannot be empty.")
        return v
    @field_validator("terms")
    @classmethod
    def clean_terms(cls,v): return [x.strip() for x in v if x and x.strip()]
class DocumentResponse(BaseModel):
    text:str; source:str; model:str|None=None
@router.post("/generate",response_model=DocumentResponse)
def generate_document(request:DocumentRequest):
    try:
        text,source=generator.generate_document(request.document_type,request.parties,request.terms,request.effective_date)
        return DocumentResponse(text=text[:MAX_DOCUMENT_CHARS],source=source,model=generator.model if source=="gemini" else None)
    except Exception as exc: raise HTTPException(status_code=502,detail=f"Document generation failed: {exc}") from exc
