import os
from typing import Optional

#
from src.domain.classes import VideoCodecs
from src.application.use_cases.download import UC_Download


class UC_VideoDownload(UC_Download):

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
            duration_limits={  # calidad
                "480": 16,
                "720": 12,
                "1080": 8,
                "1440": 4,
            },
            quality=quality,
            codec=VideoCodecs.MP4.value,
            file_type="video",
        )
