from unittest.mock import ANY


def test_upload_document_success(mock_db, mock_ocr, client, mock_doc_service):
    # 1Simulate Parseur's response structure
    mock_ocr.upload_to_parseur.return_value = {
        "message": "OK",
        "attachments": [
            {
                "name": "LES GEANTS",
                "DocumentID": "4f78e3c9894e4f6ca6d9655d9bf3ab15"
            }
        ]
    }
    mock_doc_service.create_document.return_value = {
        "status": "pending",
        "document_id": "4f78e3c9894e4f6ca6d9655d9bf3ab15",
        "filename": "LES GEANTS",
        "extracted_data": None
    }

    # 2. Prepare the "File" for the request
    file_content = b"fake pdf content"
    files = {"file": ("test.pdf", file_content, "application/pdf")}
    data = {"filename": "test.pdf"}

    # 3. Execute the request
    # Note: For Form/File, we use 'data' and 'files' arguments
    response = client.post("/api/v1/ocr/upload", data=data, files=files)

    # 4. Assertions
    assert response.json()["status"] == "pending"
    assert response.status_code == 200

    # Verify the OCR service was called with the right bytes
    mock_ocr.upload_to_parseur.assert_called_once()

    # Verify the Document service was called with the right bytes
    mock_doc_service.create_document.assert_called_once()


def test_handle_webhook_success(client, mock_db, mock_doc_service):
    # 1. Create a mock for the DocumentService

    # Simulate finding a document in the DB
    mock_doc_service.get_doc_by_id.return_value = {
        "status": "pending",
        "document_id": "4f78e3c9894e4f6ca6d9655d9bf3ab15",
        "filename": "LES GEANTS",
        "extracted_data": None
    }

    # 3. Define the Parseur payload
    payload = {
        "buyer_name": "ED THOMPSON",
        "delivery_date": "03242026",
        "extension_total": 30696.78,
        "grand_total": 30696.78,
        "line_items": [
            {
                "product_supplier_code": "107813",
                "product_description": "PAPER BAGS BROWN 6LB",
                "barcode_id": "62847602790508",
                "quantity_ordered": 42.0,
                "cost": 31.8
            },
            {
                "product_supplier_code": "107888",
                "product_description": "PAPER BAGS BROWN 12LB",
                "barcode_id": "62847602790805",
                "quantity_ordered": 10.0,
                "cost": 60.67
            },
            {
                "product_supplier_code": "107896",
                "product_description": "PAPER BAGS BROWN 14LB 7.75 X 4.75 X 1298",
                "barcode_id": "62847602791208",
                "quantity_ordered": 10.0,
                "cost": 62.31
            },
            {
                "product_supplier_code": "136333",
                "product_description": "PAN LINER SILICONE SUPERIOR 18.5 X 26",
                "barcode_id": "62847601441520",
                "quantity_ordered": 6.0,
                "cost": 241.56
            },
            {
                "product_supplier_code": "162677",
                "product_description": "PAPER BAGS 50 LB 12 X 7 X 17",
                "barcode_id": "62847602791703",
                "quantity_ordered": 15.0,
                "cost": 131.81
            },
            {
                "product_supplier_code": "162727",
                "product_description": "PAPER BAGS SINGLE LIQUOR 6 X 2 X 15",
                "barcode_id": "62847602792007",
                "quantity_ordered": 10.0,
                "cost": 73.61
            },
            {
                "product_supplier_code": "278911",
                "product_description": "SANDWICH BAG GIANT 6X2X9 WHITE GREASE",
                "barcode_id": "62847601404010",
                "quantity_ordered": 14.0,
                "cost": 67.77
            },
            {
                "product_supplier_code": "279000",
                "product_description": "FOIL HOT DOG BAGS PLAIN 7\"X 1.5\"X 5.5",
                "barcode_id": "62847601442280",
                "quantity_ordered": 16.0,
                "cost": 144.17
            },
            {
                "product_supplier_code": "280408",
                "product_description": "SANDWICH BAG BROWN GRS PROOF 6 3/4 6",
                "barcode_id": "62847601442270",
                "quantity_ordered": 16.0,
                "cost": 33.63
            },
            {
                "product_supplier_code": "310649",
                "product_description": "STEAK PAPER BLACK 8\"X11\"",
                "barcode_id": "62847601439270",
                "quantity_ordered": 16.0,
                "cost": 52.13
            },
            {
                "product_supplier_code": "310730",
                "product_description": "PAN LINER SILICONE SUPERIOR 16\"X 24\"",
                "barcode_id": "00770238090110",
                "quantity_ordered": 24.0,
                "cost": 199.3
            },
            {
                "product_supplier_code": "325191",
                "product_description": "FRENCH FRY BAG 6X1X5",
                "barcode_id": "62847602779800",
                "quantity_ordered": 5.0,
                "cost": 89.04
            },
            {
                "product_supplier_code": "360313",
                "product_description": "PAPER BAGS 50LB 12X7X17 RETAIL",
                "barcode_id": "62847602791703",
                "quantity_ordered": 18.0,
                "cost": 52.03
            },
            {
                "product_supplier_code": "360321",
                "product_description": "PAPER BAGS 65LB 12X7X17 RETAIL",
                "barcode_id": "62847602791109",
                "quantity_ordered": 18.0,
                "cost": 57.51
            },
            {
                "product_supplier_code": "393736",
                "product_description": "LINER BASKET BLACK CHECK 12\"X12\"",
                "barcode_id": "62847631438650",
                "quantity_ordered": 12.0,
                "cost": 69.08
            },
            {
                "product_supplier_code": "393751",
                "product_description": "LINER BASKET NEWSPRINT 12\"x12\"",
                "barcode_id": "62847601443910",
                "cost": 160.17
            },
            {
                "product_supplier_code": "474056",
                "product_description": "C/CHEF FRENCH FRY BAG 5X1X5",
                "barcode_id": "10628476027785",
                "cost": 46.14
            },
            {
                "product_supplier_code": "491191",
                "product_description": "FSP WAX PAPER LINER 12X12",
                "barcode_id": "62847602814600",
                "quantity_ordered": 9.0,
                "cost": 145.11
            },
            {
                "product_supplier_code": "538827",
                "product_description": "C/CHEF PIZZA LINERS 15 X 15",
                "barcode_id": "62847602789760",
                "quantity_ordered": 11.0,
                "cost": 76.87
            },
            {
                "product_supplier_code": "624130",
                "product_description": "PAN LINER QUILON LARGE 16.4\"X24.4\"",
                "barcode_id": "62847601406420",
                "quantity_ordered": 24.0,
                "cost": 128.53
            },
            {
                "product_supplier_code": "720912",
                "product_description": "FOIL SHEETS 12X12 CUSH FOLD",
                "barcode_id": "62847601139162",
                "quantity_ordered": 24.0,
                "cost": 88.84
            },
            {
                "product_supplier_code": "720920",
                "product_description": "FOIL SHEETS 10X10 CUSH FOLD",
                "barcode_id": "00770238811753",
                "quantity_ordered": 6.0,
                "cost": 82.02
            },
            {
                "product_supplier_code": "753756",
                "product_description": "SANDWICH BAG REG 6-3/4X6-3/4 WHITE",
                "barcode_id": "62847601403380",
                "quantity_ordered": 16.0,
                "cost": 33.63
            },
            {
                "product_supplier_code": "781849",
                "product_description": "FREEZER PAPER 24\" X 240M",
                "barcode_id": "62847601371530",
                "quantity_ordered": 15.0,
                "cost": 105.55
            }
        ],
        "order_date": "03102026",
        "purchase_order_number": "963819",
        "supplier_id": "50990",
        "supplier_name": "MONTREAL PAPER CUTTING",
        "supplier_phone": "514-765-0990",
        "customer_name": "PRATTS LIMITED",
        "delivery_address": "101 HUTCHINGS STREET WINNIPEG, MANITOBA R2X 2V4",
        "DocumentID": "4f78e3c9894e4f6ca6d9655d9bf3ab15"
    }

    # 4. Execute
    response = client.post("/webhook/parseur", json=payload)

    # 5. Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "document received"}

    # Verify the service methods were called correctly
    mock_doc_service.get_doc_by_id.assert_called_once_with("4f78e3c9894e4f6ca6d9655d9bf3ab15")
    mock_doc_service.update_document_with_extraction.assert_called_once()


def test_handle_webhook_not_found(client, mock_db, mock_doc_service):

    mock_doc_service.get_doc_by_id.return_value = None  # Document doesn't exist

    response = client.post("/webhook/parseur", json={"DocumentID": "unknown_id"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"


def test_normalise_document_correct_product_code(client, mock_prod_repo, mock_normalise_service, mock_doc_service):
    mock_normalise_service.normalize_doc.return_value = {
        "customer_number": "100600",
        "purchase_order_number": "5500009696",
        "order_date": "2026-04-05",
        "expected_ship_date": "2026-04-10",
        "ship_to_name": "ship to name",
        "ship_to_address_line_1": "address",
        "ship_to_city": "city",
        "is_fully_normalized": "False",
        "total_items_needing_review": 0,
        "order_details": []
    }

    mock_doc_service.get_doc_by_id.return_value = {
        "status": "pending",
        "document_id": "4f78e3c9894e4f6ca6d9655d9bf3ab15",
        "filename": "LES GEANTS",
        "extracted_data": {
            "buyer_name": "ED THOMPSON",
            "delivery_date": "03242026",
            "extension_total": 30696.78,
            "grand_total": 30696.78,
            "line_items": [
                {
                    "product_supplier_code": "K-01-400-KC-R-3600",
                    "product_description": "PAPER BAGS BROWN 6LB",
                    "barcode_id": "62847602790508",
                    "quantity_ordered": 42.0,
                    "cost": 31.8
                },
                {
                    "product_supplier_code": "107888",
                    "product_description": "PAPER BAGS BROWN 12LB",
                    "barcode_id": "62847602790805",
                    "quantity_ordered": 10.0,
                    "cost": 60.67
                },
                {
                    "product_supplier_code": "107896",
                    "product_description": "PAPER BAGS BROWN 14LB 7.75 X 4.75 X 1298",
                    "barcode_id": "62847602791208",
                    "quantity_ordered": 10.0,
                    "cost": 62.31
                },
                {
                    "product_supplier_code": "136333",
                    "product_description": "PAN LINER SILICONE SUPERIOR 18.5 X 26",
                    "barcode_id": "62847601441520",
                    "quantity_ordered": 6.0,
                    "cost": 241.56
                },
                {
                    "product_supplier_code": "162677",
                    "product_description": "PAPER BAGS 50 LB 12 X 7 X 17",
                    "barcode_id": "62847602791703",
                    "quantity_ordered": 15.0,
                    "cost": 131.81
                },
                {
                    "product_supplier_code": "162727",
                    "product_description": "PAPER BAGS SINGLE LIQUOR 6 X 2 X 15",
                    "barcode_id": "62847602792007",
                    "quantity_ordered": 10.0,
                    "cost": 73.61
                },
                {
                    "product_supplier_code": "278911",
                    "product_description": "SANDWICH BAG GIANT 6X2X9 WHITE GREASE",
                    "barcode_id": "62847601404010",
                    "quantity_ordered": 14.0,
                    "cost": 67.77
                },
                {
                    "product_supplier_code": "279000",
                    "product_description": "FOIL HOT DOG BAGS PLAIN 7\"X 1.5\"X 5.5",
                    "barcode_id": "62847601442280",
                    "quantity_ordered": 16.0,
                    "cost": 144.17
                },
                {
                    "product_supplier_code": "280408",
                    "product_description": "SANDWICH BAG BROWN GRS PROOF 6 3/4 6",
                    "barcode_id": "62847601442270",
                    "quantity_ordered": 16.0,
                    "cost": 33.63
                },
                {
                    "product_supplier_code": "310649",
                    "product_description": "STEAK PAPER BLACK 8\"X11\"",
                    "barcode_id": "62847601439270",
                    "quantity_ordered": 16.0,
                    "cost": 52.13
                },
                {
                    "product_supplier_code": "310730",
                    "product_description": "PAN LINER SILICONE SUPERIOR 16\"X 24\"",
                    "barcode_id": "00770238090110",
                    "quantity_ordered": 24.0,
                    "cost": 199.3
                },
                {
                    "product_supplier_code": "325191",
                    "product_description": "FRENCH FRY BAG 6X1X5",
                    "barcode_id": "62847602779800",
                    "quantity_ordered": 5.0,
                    "cost": 89.04
                },
                {
                    "product_supplier_code": "360313",
                    "product_description": "PAPER BAGS 50LB 12X7X17 RETAIL",
                    "barcode_id": "62847602791703",
                    "quantity_ordered": 18.0,
                    "cost": 52.03
                },
                {
                    "product_supplier_code": "360321",
                    "product_description": "PAPER BAGS 65LB 12X7X17 RETAIL",
                    "barcode_id": "62847602791109",
                    "quantity_ordered": 18.0,
                    "cost": 57.51
                },
                {
                    "product_supplier_code": "393736",
                    "product_description": "LINER BASKET BLACK CHECK 12\"X12\"",
                    "barcode_id": "62847631438650",
                    "quantity_ordered": 12.0,
                    "cost": 69.08
                },
                {
                    "product_supplier_code": "393751",
                    "product_description": "LINER BASKET NEWSPRINT 12\"x12\"",
                    "barcode_id": "62847601443910",
                    "cost": 160.17
                },
                {
                    "product_supplier_code": "474056",
                    "product_description": "C/CHEF FRENCH FRY BAG 5X1X5",
                    "barcode_id": "10628476027785",
                    "cost": 46.14
                },
                {
                    "product_supplier_code": "491191",
                    "product_description": "FSP WAX PAPER LINER 12X12",
                    "barcode_id": "62847602814600",
                    "quantity_ordered": 9.0,
                    "cost": 145.11
                },
                {
                    "product_supplier_code": "538827",
                    "product_description": "C/CHEF PIZZA LINERS 15 X 15",
                    "barcode_id": "62847602789760",
                    "quantity_ordered": 11.0,
                    "cost": 76.87
                },
                {
                    "product_supplier_code": "624130",
                    "product_description": "PAN LINER QUILON LARGE 16.4\"X24.4\"",
                    "barcode_id": "62847601406420",
                    "quantity_ordered": 24.0,
                    "cost": 128.53
                },
                {
                    "product_supplier_code": "720912",
                    "product_description": "FOIL SHEETS 12X12 CUSH FOLD",
                    "barcode_id": "62847601139162",
                    "quantity_ordered": 24.0,
                    "cost": 88.84
                },
                {
                    "product_supplier_code": "720920",
                    "product_description": "FOIL SHEETS 10X10 CUSH FOLD",
                    "barcode_id": "00770238811753",
                    "quantity_ordered": 6.0,
                    "cost": 82.02
                },
                {
                    "product_supplier_code": "753756",
                    "product_description": "SANDWICH BAG REG 6-3/4X6-3/4 WHITE",
                    "barcode_id": "62847601403380",
                    "quantity_ordered": 16.0,
                    "cost": 33.63
                },
                {
                    "product_supplier_code": "781849",
                    "product_description": "FREEZER PAPER 24\" X 240M",
                    "barcode_id": "62847601371530",
                    "quantity_ordered": 15.0,
                    "cost": 105.55
                }
            ],
            "order_date": "03102026",
            "purchase_order_number": "963819",
            "supplier_id": "50990",
            "supplier_name": "MONTREAL PAPER CUTTING",
            "supplier_phone": "514-765-0990",
            "customer_name": "PRATTS LIMITED",
            "delivery_address": "101 HUTCHINGS STREET WINNIPEG, MANITOBA R2X 2V4",
            "DocumentID": "4f78e3c9894e4f6ca6d9655d9bf3ab15"
        }
    }

    mock_prod_repo.get_product_by_customer_and_price.return_value = [
        {
            "customer": "LES GEANTS DU COUVRE-PLANCHER",
            "date": "2022-06-23",
            "item": "K-01-400-KC-R-3600",
            "product": "36\" POLY COATED LATEX (400 SQ.FT.)",
            "price": 19.3,
            "ship_to_name": "LES GEANTS DU COUVRE-PLANCHER",
            "ship_to_address_1": "INC.",
            "ship_to_address_2": "789, 2IEME RUE",
            "ship_to_address_3": "NaN",
            "ship_to_address_4": "NaN",
            "ship_to_city": "ST-JEAN SUR RICHELIEU",
            "ship_to_state": "QC.",
            "ship_to_zip": "J2X 3H7",
            "ship_to_country": "CANADA"
        }
    ]
    mock_prod_repo.get_products_by_product_code.return_value = [
        {
            "customer": "LES GEANTS DU COUVRE-PLANCHER",
            "date": "2022-06-23",
            "item": "K-01-400-KC-R-3600",
            "product": "36\" POLY COATED LATEX (400 SQ.FT.)",
            "price": 19.3,
            "ship_to_name": "LES GEANTS DU COUVRE-PLANCHER",
            "ship_to_address_1": "INC.",
            "ship_to_address_2": "789, 2IEME RUE",
            "ship_to_address_3": "NaN",
            "ship_to_address_4": "NaN",
            "ship_to_city": "ST-JEAN SUR RICHELIEU",
            "ship_to_state": "QC.",
            "ship_to_zip": "J2X 3H7",
            "ship_to_country": "CANADA"
        }
    ]

    mock_prod_repo.get_products_by_description.return_value = [
        {
            "customer": "LES GEANTS DU COUVRE-PLANCHER",
            "date": "2022-06-23",
            "item": "K-01-400-KC-R-3600",
            "product": "36\" POLY COATED LATEX (400 SQ.FT.)",
            "price": 19.3,
            "ship_to_name": "LES GEANTS DU COUVRE-PLANCHER",
            "ship_to_address_1": "INC.",
            "ship_to_address_2": "789, 2IEME RUE",
            "ship_to_address_3": "NaN",
            "ship_to_address_4": "NaN",
            "ship_to_city": "ST-JEAN SUR RICHELIEU",
            "ship_to_state": "QC.",
            "ship_to_zip": "J2X 3H7",
            "ship_to_country": "CANADA"
        }
    ]

    mock_prod_repo.get_ship_to_address.return_value = {
        "customer": "LES GEANTS DU COUVRE-PLANCHER",
        "date": "2022-06-23",
        "item": "K-01-400-KC-R-3600",
        "product": "36\" POLY COATED LATEX (400 SQ.FT.)",
        "price": 19.3,
        "ship_to_name": "LES GEANTS DU COUVRE-PLANCHER",
        "ship_to_address_1": "INC.",
        "ship_to_address_2": "789, 2IEME RUE",
        "ship_to_address_3": "NaN",
        "ship_to_address_4": "NaN",
        "ship_to_city": "ST-JEAN SUR RICHELIEU",
        "ship_to_state": "QC.",
        "ship_to_zip": "J2X 3H7",
        "ship_to_country": "CANADA"
    }

    response = client.post("/api/v1/normaliser/process", json={"document_id": "4f78e3c9894e4f6ca6d9655d9bf3ab15"})

    assert response.status_code == 200
    mock_normalise_service.normalize_doc.assert_called_once()
    # mock_prod_repo.get_products_by_product_code.assert_called_once_with(ANY, ANY, "K-01-400-KC-R-3600")


