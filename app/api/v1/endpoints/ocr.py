from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from app.schemas.OcrDocumentSchema import OcrDocumentSchema
from app.services.documentservice import DocumentService
from app.services.ocr_service import OCRService, get_ocr_service

from app.utils.DocumentState import DocumentState

router = APIRouter()


@router.post("/upload", response_model=OcrDocumentSchema)
async def upload_document(filename: str = Form(...),
                          file: UploadFile = File(...),
                          ocr_service: OCRService = Depends(get_ocr_service),
                          doc_service: DocumentService = Depends(),
                          ):

    if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    try:
        content = await file.read()
        data = await ocr_service.upload_to_parseur(file_content=content, filename=filename)
        added_doc = doc_service.create_document(
            document_id=str(data['attachments'][0]['DocumentID']),
            filename=filename,
            status=DocumentState.PENDING
        )
        print("Debug (added doc): {}".format(added_doc))
        return added_doc
    except Exception as e:
        print("Error: " + str(e))
        raise HTTPException(status_code=500, detail="unable to upload doc!")


# @router.get("/document/{document_id}")
# async def get_document(document_id: str,
#                        ocr_service: OCRService = Depends(get_ocr_service),
#                        db: Session = Depends(get_db)):
#     data = json.loads((await ocr_service.get_parsed_document(document_id=document_id))["result"])
#     purchase_order = PODataExtract()
#     purchase_order.delivery_address = data.get("delivery_address")
#     purchase_order.order_date = data.get("order_date")
#     purchase_order.buyer_phone = data.get("buyer_phone")
#     purchase_order.delivery_date = data.get("delivery_date")
#     purchase_order.grand_total = data.get("grand_total")
#     purchase_order.customer_name = data.get("customer_name")
#
#     purchase_order.supplier_name = data.get("supplier_name")
#     purchase_order.buyer_email = data.get("buyer_email")
#
#     if data.get("line_items"):
#         for item in data["line_items"]:
#             line_item = PODataExtractItem()
#             line_item.po_id = purchase_order.id
#             line_item.product_supplier_code = item.get("product_supplier_code")
#             line_item.product_description = item.get("product_description")
#             line_item.quantity_ordered = item.get("quantity_ordered")
#             line_item.cost = item.get("cost")
#             purchase_order.items.append(line_item)
#
#     db.add(purchase_order)
#     db.commit()
#
#     return data
