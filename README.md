# API de Sentimiento en Docker

Demo: empaquetar una API de FastAPI (con un modelo de machine learning) dentro
de un contenedor de Docker, correrla, y desplegarla gratis en Render.
El "solo corre en mi máquina", resuelto.

El modelo es **scikit-learn puro**: TF-IDF + Regresión Logística, 102 KB.
Sin PyTorch, sin transformers, sin GPU. La imagen completa pesa ~250 MB y entra
sobrada en los 512 MB de RAM del plan gratuito de Render.

## Estructura
```
api-en-docker/
├── src/
│   ├── datos.py        # el dataset: 210 reseñas etiquetadas a mano
│   ├── entrenar.py     # entrena el modelo y lo guarda en modelo.joblib
│   └── api.py          # la API de FastAPI
├── Dockerfile          # la receta para empaquetarla
├── .dockerignore       # qué NO meter en la caja
├── render.yaml         # config de despliegue en Render
├── requirements.txt    # las dependencias
└── README.md
```

## Los dos comandos

```bash
# 1. Construir la imagen (lee el Dockerfile — aquí se entrena el modelo)
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

```json
{"texto": "Me encantó este curso", "sentimiento": "POSITIVO", "confianza": 0.9846}
```

Hay tres endpoints: `GET /` (¿está viva?), `GET /modelo` (qué hay dentro del
modelo) y `POST /analizar`.

## Desplegar en Render (plan gratuito)

1. Sube el repo a GitHub.
2. En Render: **New > Blueprint**, conecta el repo. El `render.yaml` ya le dice
   todo lo que necesita saber.
3. Espera el build (~2 min) y listo.

Dos cosas del plan gratuito que conviene saber: el servicio **se duerme** tras
15 minutos sin tráfico y tarda ~30 s en despertar, y Render decide el puerto —
por eso el `CMD` del Dockerfile usa `${PORT:-8000}` en vez de un 8000 fijo.

## Correrlo sin Docker (para desarrollar)

```bash
pip install -r requirements.txt
python -m src.entrenar          # genera src/modelo.joblib
uvicorn src.api:app --reload
```

## Notas sobre el modelo

**Qué tan bueno es:** 91.3% ± 4.0% de accuracy en validación cruzada. Para 210
frases de entrenamiento y 102 KB de modelo, está bien. No espere más: no
entiende sarcasmo, ni negaciones ("no está mal"), ni contexto.

**El dataset importa más que el modelo.** La primera versión de `datos.py` tenía
108 frases con vocabulario deliberadamente variado, y el modelo se quedó en 62%
— apenas mejor que lanzar una moneda. Probamos 16 combinaciones de
vectorizador y clasificador: todas daban entre 60% y 65%. Lo que subió el
número a 91% no fue cambiar el modelo, fue reescribir los datos para que el
vocabulario **se repitiera** entre frases. Con datasets chicos, si cada ejemplo
usa palabras únicas, una frase nueva no tiene nada en común con lo que el
modelo vio.

**Por qué mira letras y no solo palabras.** El pipeline en `entrenar.py` usa dos
vectorizadores pegados: uno de palabras y uno de trozos de 3 a 5 letras. El
segundo es el que permite que el modelo acierte en `"rapidísimo"`,
`"decepcionante"` o `"recomendadísimo"` — palabras que nunca vio, pero que
comparten pedazos con `"rápido"`, `"decepción"` y `"recomiendo"`.
