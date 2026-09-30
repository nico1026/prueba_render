# 1. Partimos de una imagen con Python 3.12 ya instalado (versión ligera)
FROM python:3.12-slim

# 2. Trabajamos dentro de la carpeta /app del contenedor
WORKDIR /app

# 3. Copiamos SOLO la lista de dependencias primero (truco del caché)
COPY requirements.txt .

# 4. Instalamos las dependencias dentro del contenedor
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto del código (la carpeta src/)
COPY src/ ./src/

# 6. Entrenamos el modelo AQUÍ, durante el build.
#    Así la imagen sale con el modelo ya adentro: el contenedor arranca en
#    milisegundos y no necesita internet para funcionar.
RUN python -m src.entrenar

# 7. Avisamos que la app usa el puerto 8000
EXPOSE 8000

# 8. Al arrancar el contenedor, levantamos la API con uvicorn.
#    Ojo con ${PORT:-8000}: Render decide el puerto y lo inyecta como variable
#    de entorno. Localmente no existe, y ahí usamos 8000.
CMD uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000}
