# 💻 Backend de MOPI

-----

## 🐍 Desarrollo en Entorno Local (Windows) 🖥️

Si necesitas trabajar con el proyecto sin usar Docker, es vital gestionar las dependencias directamente con `pip` y un entorno virtual.

### Pre-requisitos

Antes de comenzar, debes tener instalado **FFmpeg** en tu sistema.

### Gestión de Dependencias

Abre una terminal (**PowerShell** o **CMD**) en el directorio raíz del proyecto para configurar el entorno virtual y las dependencias.

| Tarea | Comando (PowerShell/CMD) | Descripción |
| :--- | :--- | :--- |
| **Crear Entorno** | `python -m venv .venv` | Crea un nuevo entorno virtual llamado `.venv`. |
| **Activar Entorno** | `.\.venv\Scripts\activate` | Activa el entorno. Verás `(.venv)` en el *prompt* de tu terminal. |
| **Instalar Dependencias** | `pip install -r requirements.txt` | Instala todas las librerías listadas en el archivo. |
| **Desactivar Entorno** | `deactivate` | Sale del entorno virtual, volviendo al entorno global. |

### Mantenimiento y Actualización de Dependencias

Mantener tu entorno virtual al día es crucial para la consistencia del desarrollo.

  * **Actualizar PIP:** Asegúrate de que tu gestor de paquetes esté al día.

    ```bash
    python -m pip install --upgrade pip
    ```

  * **Sincronizar `requirements.txt`:** Después de cualquier instalación o actualización de dependencias, debes reflejar los cambios en el archivo.

    ```bash
    pip freeze > requirements.txt
    ```

el archivo .env debe ir dentro de la carpeta app

ejecutar
fastapi dev main.py

# Borrar carpetas __pycache__ (usando powershell)
Get-ChildItem -Path . -Include __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force
-----

## 🐳 Configuración y Uso con Docker

El servicio se levanta usando el archivo `docker-compose.yml` que ya se encuentra en el proyecto.

### API

Para levantar el servicio de la API, asegúrate de que las líneas relacionadas con servicios de caché o externos no necesarios estén comentadas en el `docker-compose.yml`.

Para iniciar el servicio, ejecuta el siguiente comando en el directorio raíz del proyecto:

```bash
docker compose up -d
```

> **Nota:** La bandera `-d` (**detached**) permite que los contenedores se ejecuten en segundo plano, liberando tu terminal.

Para verificar que los contenedores estén corriendo, usa:

```bash
docker ps
```

Deberías ver el contenedor principal, nombrado `cont-apimopi`.

### Acceso al Servicio

Una vez que los contenedores estén activos, el servicio estará disponible en **[http://localhost:8000](http://localhost:8000)** y la documentación de la API (si está configurada) en **[http://localhost:8000/docs](http://localhost:8000/docs)**.

### 2.3. Comandos Útiles de Docker

Aquí tienes comandos esenciales para gestionar tu entorno Docker, usando el nombre de contenedor `cont-apimopi` y de imagen `iso-apimopi` como ejemplo.

| Comando | Descripción |
| :--- | :--- |
| `docker compose up -d` | **Inicia** los servicios en segundo plano definidos en `docker-compose.yml`. |
| `docker compose down` | **Detiene y elimina** contenedores, redes e imágenes definidos en el `docker-compose.yml`. |
| `docker compose restart` | **Reinicia** todos los servicios definidos en el archivo de composición. |
| `docker stop cont-apimopi` | **Detiene** la ejecución del contenedor de la API. |
| `docker start cont-apimopi` | **Reinicia** un contenedor que ha sido detenido. |
| `docker logs -f cont-apimopi` | Muestra los **logs** en tiempo real (`-f` por *follow*) del contenedor de la API. |
| `docker rm cont-apimopi` | **Elimina** el contenedor de la API. **Debe estar detenido primero.** |
| `docker build -t iso-apimopi .` | Construye o reconstruye la **imagen** del backend usando el `Dockerfile`. |
| `docker rmi iso-apimopi` | **Elimina** la imagen localmente. **Detén los contenedores antes de eliminar la imagen.** |
| `docker ps -a` | Muestra **todos los contenedores** (activos y detenidos). |

-----

## 3\. 🚀 Despliegue

Para un despliegue en un entorno de producción o *staging*, debes considerar lo siguiente:

  * **Cookies para YouTube:**
    Para procesar videos de YouTube, crea un archivo **`cookies.txt`** dentro de la carpeta `app`. Revisa la [documentación de yt-dlp](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp) para saber cómo obtener las *cookies* de tu navegador.
