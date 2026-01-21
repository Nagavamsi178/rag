import os
from pathlib import Path
from security.permissions import can_view_document

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_DATA_DIR = PROJECT_ROOT / "data"


def get_user_dir(username: str) -> Path:
    path = BASE_DATA_DIR / username
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_uploaded_file(uploaded_file, user_dir: Path) -> Path:
    file_path = user_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def list_accessible_pdfs(role, current_user) -> list[str]:
    pdfs = []

    for user_dir in BASE_DATA_DIR.iterdir():
        if not user_dir.is_dir():
            continue

        owner = user_dir.name
        if not can_view_document(role, owner, current_user):
            continue

        for file in user_dir.iterdir():
            if file.suffix.lower() == ".pdf":
                pdfs.append(f"{owner}/{file.name}")

    return pdfs

def resolve_pdf_path(
    pdf_ref: str,
    role: str,
    current_user: str
) -> Path:
    owner, filename = pdf_ref.split("/", 1)
    if not can_view_document(role, owner, current_user):
        raise PermissionError("Unauthorized access")

    pdf_path = BASE_DATA_DIR / owner / filename
    if not pdf_path.exists():
        raise FileNotFoundError("PDF not found")

    return pdf_path
