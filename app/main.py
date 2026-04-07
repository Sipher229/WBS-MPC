from app.api.v1.endpoints import ocr, normaliser, documents
from fastapi import FastAPI, Depends, HTTPException
from app.database import engine, Base
from app.services.documentservice import DocumentService

app = FastAPI(title="Workflow Bridging System API")
# Include the OCR routes
app.include_router(ocr.router, prefix="/api/v1/ocr", tags=["OCR"])
app.include_router(normaliser.router, prefix="/api/v1/normaliser", tags=["NORMALISER"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["DOCUMENTS"])

Base.metadata.create_all(bind=engine)


@app.post("/webhook/parseur")
def handle_webhook(
        payload: dict,
        doc_service: DocumentService = Depends()
):
    doc_id = str(payload.get("DocumentID"))

    # 1. Fetch the tracker
    doc = doc_service.get_doc_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # 2. Perform the update
    try:
        doc_service.update_document_with_extraction(doc, payload)
    except Exception:
        # Log the actual error 'e' here for debugging
        raise HTTPException(status_code=500, detail="Internal server error")

    return {"message": "document received"}


@app.get("/")
async def root():
    return {"message": "OCR Service is Online"}

