from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

#
from core.settings import settings
from src.presentation.filter_exception import filter_exception
from src.presentation.routes import router


# fastapi dev app/main.py
#
# cd app
# fastapi dev main.py


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)


# Registrar el filtro global de excepciones
filter_exception(app)


# Middleware para corregir esquema HTTPS si viene tras proxy
@app.middleware("http")
async def https_scheme(request: Request, call_next):
    proto = request.headers.get("X-Forwarded-Proto", "").lower()
    if proto == "https":
        request.scope["scheme"] = "https"
    return await call_next(request)


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*" if not settings.APP_CLIENT else settings.APP_CLIENT],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


# Incluir otros endpoint
app.include_router(router)


# run run
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
