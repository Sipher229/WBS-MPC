import re

PROD_CODE_PATTERN = re.compile(
    r"^[A-Z]-?\d+-?\d+-?[A-Z]+-?[A-Z]*-?\d+$",
    re.IGNORECASE
)
test_code = "K-01-400-KC-R-3600"

print(f"test code passes: {bool(PROD_CODE_PATTERN.fullmatch(test_code))}")
