import requests
from pathlib import Path

def download_hf_pdf(
    repo_id: str,
    filename: str,
    target_dir: str,
    repo_type: str = "dataset",
):
    """
    Safely download PUBLIC Hugging Face PDFs (no 403).
    """
    url = f"https://huggingface.co/{repo_id}/resolve/main/{filename}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
    }

    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    file_path = target_dir / filename

    if file_path.exists():
        return file_path

    r = requests.get(url, headers=headers, stream=True, timeout=30)

    if r.status_code != 200:
        raise RuntimeError(f"HF download failed: {r.status_code}")

    with open(file_path, "wb") as f:
        for chunk in r.iter_content(8192):
            if chunk:
                f.write(chunk)

    return file_path
