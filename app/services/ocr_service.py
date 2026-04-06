import niquests
from sqlalchemy.orm import Session
from app.core.config import settings

_ocr_service = None
PARSEUR_URL = "https://api.parseur.com"
AUTH_HEADERS = {"Authorization": f"Token {settings.PARSEUR_API_KEY}"}


class OCRService:
    @staticmethod
    async def upload_to_parseur(file_content: bytes, filename: str = "customer_PO"):
        headers = AUTH_HEADERS
        files = {'file': (filename, file_content)}
        # print("uploading doc...")
        async with niquests.AsyncSession() as client:
            response = await client.post(
                f"{PARSEUR_URL}/parser/{settings.PARSEUR_MAILBOX_ID}/upload",
                headers=headers,
                files=files
            )
            response.raise_for_status()
            data = response.json()
            # print(f"DEBUG: Data received is {data}")

            return data

    @staticmethod
    async def get_parsed_document(document_id: str):
        print("getting document...")

        async with niquests.AsyncSession() as client:

            response = await client.get(f"{PARSEUR_URL}/document/{document_id}?with_result=true", headers=AUTH_HEADERS)
            response.raise_for_status()
            data = response.json()
            print("document received")
            return data


def get_ocr_service():
    global _ocr_service
    if _ocr_service is None:
        _ocr_service = OCRService()
    return _ocr_service
