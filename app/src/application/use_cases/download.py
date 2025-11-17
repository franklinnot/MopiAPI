import re
from typing import Optional, Literal
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import asyncio

#
from core.settings import settings
from core.logger import logger
from src.domain.classes import AllPlatforms
from src.application.responses import validResponse, errorResponse, Respuesta
from src.application.responses import RES_FileResponse
from src.infraestructure.dlp import dlp
from src.application.utils.utils import utils

executor = ThreadPoolExecutor(max_workers=5)


class UC_Download:

    def __init__(
        self,
        url: str,
        title: Optional[str],
        platform: str,
        duration_limits: dict,
        quality: str,
        codec: str,
        file_type: Literal["audio", "video"],
    ):
        self.url = url
        self.title = title
        self.platform = platform
        self.duration_limits = duration_limits
        self.quality = quality
        self.codec = codec
        self.file_type = file_type
        #
        self.folder_path: str = ""  # path de la carpeta que alojara el archivo
        self.file_path: str = ""  # path completo: folder + filename.ext
        self.file_name: str = ""  # nombre del archivo
        self.extension: str = (
            ""  # extension del archivo (en caso de no coincidir con el codec)
        )

    def verify_title(self) -> bool:
        """Valida que el título sea aceptable (sin caracteres prohibidos y con longitud <= 64)."""
        if not self.title:
            return False

        invalid_chars = r'[<>:"/\\|?*\n\r\t]'
        title = self.title.strip()
        if re.search(invalid_chars, title) or len(title) > 64:
            return False
        return True

    def verify_all(self) -> str:
        result = False
        # verificar el titulo, de ser necesario
        if self.title != None:
            result = self.verify_title()
            if not result:
                return "El título no es válido"

        # verificar si el dominio de la url coincide con la plataforma indicada
        result = utils.verify_domain(self.url, self.platform)
        if not result:
            return "La url no es válida"

        if self.platform == AllPlatforms.YOUTUBE.value:
            result = utils.format_url_youtube(self.url)
            if not result:
                return "La url no es válida"
            self.url = result

        # si se ejecuta en desarrollo, no verificamos la duracion
        if settings.ENVIRONMENT == "dev":
            return ""

        # verificar si la duracion es valida
        result = dlp.verify_duration(self.url, self.duration_limits, self.quality)
        if result:
            return result

        return ""

    def download(self) -> bool:
        self.folder_path = utils.create_temp_folder()

        self.file_path, self.file_name, self.extension = dlp.download(
            url=self.url,
            folder_path=self.folder_path,
            file_type=self.file_type,
            allowed_exts=[self.codec],
            codec=self.codec,
            quality=self.quality,
        )

        if not self.file_path:
            return False
        return True

    def execute(self) -> Respuesta:
        # verificar los datos de entrada
        result = self.verify_all()
        if result:
            return errorResponse(result)

        # descargamos
        if not self.download():
            return errorResponse()

        base64 = utils.to_base64(self.file_path)
        utils.delete_temp_folder(Path(self.folder_path).name)  # borramos la carpeta

        return validResponse(
            RES_FileResponse(
                title=self.title if self.title else self.file_name,
                extension=self.extension,
                base64=base64,
            )
        )

    def safe_execute(self) -> Respuesta:
        try:
            return self.execute()
        except Exception as e:
            logger.exception(e)
            return errorResponse()

    async def execute_parallel(self) -> Respuesta:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, self.safe_execute)
