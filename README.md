# API de Sentimiento en Docker

Demo: empaquetar una API de FastAPI (con un modelo de Hugging Face) dentro de un
contenedor de Docker, y correrla. El "solo corre en mi máquina", resuelto.

## Estructura
```
api-en-docker/
├── src/
│   └── api.py          # la API de FastAPI
├── Dockerfile          # la receta para empaquetarla
├── .dockerignore       # qué NO meter en la caja
├── requirements.txt    # las dependencias
└── README.md
```

## Los dos comandos

```bash
# 1. Construir la imagen (lee el Dockerfile)
docker build -t api-sentimiento .

# 2. Correr un contenedor desde la imagen
docker run -p 8000:8000 api-sentimiento
```

La API queda viva en http://localhost:8000 — y su documentación interactiva en
http://localhost:8000/docs

## Probarla

```bash
curl -X POST http://localhost:8000/analizar \
  -H "Content-Type: application/json" \
  -d '{"texto": "Me encantó este curso"}'
```
