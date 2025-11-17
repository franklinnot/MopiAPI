from typing import Optional

#
from src.domain.classes import AudioCodecs
from src.application.use_cases.download import UC_Download


class UC_AudioDownload(UC_Download):
    def __init__(
        self,
        url: str,
        title: Optional[str],
        platform: str,
        quality: str,
    ):
        super().__init__(
            url=url,
            title=title,
            platform=platform,
            duration_limits={  # kbps
                "128": 16,
                "192": 12,
                "256": 8,
                "320": 4,
            },
            quality=quality,
            codec=AudioCodecs.MP3.value,
            file_type="audio",
        )
