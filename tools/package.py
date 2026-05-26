from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


CORE_OUTPUTS = [
    "seo_report.json",
    "leads.csv",
    "content_package.json",
    "outreach_kit.md",
]


def package_outputs(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir / "marketing_package.zip"
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as archive:
        for filename in CORE_OUTPUTS:
            path = output_dir / filename
            if path.exists():
                archive.write(path, arcname=filename)
    return zip_path
