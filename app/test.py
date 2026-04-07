import re

PROD_CODE_PATTERN = re.compile(
    r"^[A-Z]-?\d+-?\d+-?[A-Z]+-?[A-Z]*-?\d+$",
    re.IGNORECASE
)
test_code = "R-05-000-DB-C-0808"

print(f"test code passes: {bool(PROD_CODE_PATTERN.fullmatch(test_code))}")
