import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
from app.main import app
from app.services.documentservice import DocumentService
from app.services.normaliser_service import NormaliserService
from app.services.ocr_service import get_ocr_service
from app.repositories.ProductRepository import ProductRepository
from app.database import get_db


@pytest.fixture
def mock_db():
    """Fixture to provide a mock database session."""
    return MagicMock()


@pytest.fixture
def mock_ocr():
    """Fixture to provide a mock OCR service."""
    return AsyncMock()


@pytest.fixture()
def mock_doc_service():
    """Fixture to provide a mock Document service"""
    return MagicMock()


@pytest.fixture()
def mock_normalise_service():
    """Fixture to provide a mock normalize service"""
    return MagicMock()


@pytest.fixture()
def mock_prod_repo():
    """Fixture to provide a mock product repo"""
    return MagicMock()


@pytest.fixture
def client(mock_db, mock_ocr, mock_doc_service, mock_normalise_service, mock_prod_repo):
    """
    Fixture that sets up the TestClient and automatically
    applies dependency overrides for every test that uses it.
    """
    # Override dependencies
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_ocr_service] = lambda: mock_ocr
    app.dependency_overrides[DocumentService] = lambda: mock_doc_service
    app.dependency_overrides[NormaliserService] = lambda: mock_normalise_service
    app.dependency_overrides[ProductRepository] = lambda: mock_prod_repo

    with TestClient(app) as c:
        yield c

    # Reset overrides after the test is finished
    app.dependency_overrides = {}
