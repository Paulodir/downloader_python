from __future__ import annotations

from pathlib import Path

import httpx


class DownloadService:
    def download(self, url: str, destination: Path, timeout: float = 30) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with httpx.stream("GET", url, timeout=timeout) as response:
            response.raise_for_status()
            with destination.open("wb") as file_obj:
                for chunk in response.iter_bytes():
                    file_obj.write(chunk)
        return destination
