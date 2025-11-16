# Versión de python -> estable
FROM python:3.13.8-slim

# Instalar dependencias en el sistema operativo -> ffmpeg
RUN apt-get update && apt-get install -y ffmpeg --no-install-recommends

# Nombramos y establecemos el directorio de trabajo
WORKDIR /code

# Copiamos el archivo de dependencias en el directorio de trabajo
COPY ./requirements.txt /code/requirements.txt

# Dentro del directorio de trabajo, instalamos todas las dependencias
# ACTUALIZADAS, tomando el archivo de dependencias.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Tomamos la carpeta 'app' y la copiamos en el directorio de trabajo
COPY ./app /code/app

# Comandos para levantar el proyecto
# En desarrollo
CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "80"]

# En producción
# CMD ["fastapi", "run", "app/main.py", "--port", "80"]